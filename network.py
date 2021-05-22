import socket
import select
import threading
import struct
import pickle

def connect(hostname, port):
    print('connect', hostname, port)
    return Network(socket.create_connection((hostname, port)))

def serve(port):
    print('serve', port)
    s = socket.create_server(('', port), family=socket.AF_INET6, dualstack_ipv6=True)
    return Network(s, True)


class PacketAssembler:
    def __init__(self):
        self.recvData = b''

    def push(self, data):
        self.recvData += data

    def pull(self):
        recvPacket = None
        if len(self.recvData) >= 4:
            length = struct.unpack_from('!I', self.recvData)[0]
            if len(self.recvData) >= 4 + length:
                recvPacket = self.recvData[4:4 + length]
                self.recvData = self.recvData[4 + length:]
                return pickle.loads(recvPacket)

    @staticmethod
    def createPacket(content):
        data = pickle.dumps(content)
        return struct.pack('!I', len(data)) + data


class Network:
    def __init__(self, s, host = False):
        self.s = s
        self.host = host
        self.clients = {}
        self.shutdown = False

        self.s.setblocking(0)

        self.lock = threading.Lock()
        self.sendPacket = None
        self.recvPacket = None
        self.sendActions = []
        self.recvActions = []

        if self.host:
            self.thread = threading.Thread(target = self.runServer)
        else:
            self.thread = threading.Thread(target = self.runClient)
        self.thread.start()

    def runServer(self):
        while True:
            inputs = [self.s] + list(self.clients)
            readable, writable, exceptional = select.select(inputs, [], inputs)
            if self.shutdown:
                return

            if self.s in readable:
                c, addr = self.s.accept()
                c.setblocking(0)
                with self.lock:
                    self.clients[c] = PacketAssembler()
                print('new client')
                readable.remove(self.s)

            for c in readable:
                try:
                    data = c.recv(4096)
                except ConnectionResetError:
                    print('drop client')
                    with self.lock:
                        del self.clients[c]
                    continue

                with self.lock:
                    if not data:
                        print('disconnect client')
                        del self.clients[c]
                    else:
                        self.clients[c].push(data)

    def runClient(self):
        a = PacketAssembler()
        while True:
            inputs = [self.s]
            readable, writable, exceptional = select.select(inputs, [], inputs, 1/30)
            if self.shutdown:
                return

            if readable:
                data = self.s.recv(4096)
                if not data:
                    print('disconnected from server')
                    return

                a.push(data)

            while True:
                packet = a.pull()
                if packet is None:
                    break

                with self.lock:
                    self.recvPacket = packet

            with self.lock:
                if self.sendActions:
                    data = PacketAssembler.createPacket(self.sendActions)
                    try:
                        self.s.sendall(data)
                        self.sendActions = []
                    except BrokenPipeError:
                        return
                    except BlockingIOError:
                        pass

    def stop(self):
        self.shutdown = True
        self.s.shutdown(socket.SHUT_RD)
        self.thread.join()

    def update(self, gameState, actions):
        if self.host:
            with self.lock:
                self.sendPacket = PacketAssembler.createPacket(gameState)
                for c in self.clients:
                    c.sendall(self.sendPacket)

                for a in self.clients.values():
                    while True:
                        packet = a.pull()
                        if packet is None:
                            break

                        actions += packet

            return gameState, actions
        else:
            with self.lock:
                self.sendActions += actions
                if self.recvPacket is not None:
                    return self.recvPacket, []
            return gameState, []

    def isHost(self):
        return self.host

    def getNumPlayers(self):
        return self.numPlayers
