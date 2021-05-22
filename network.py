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

class Network:
    def __init__(self, s, host = False):
        self.s = s
        self.host = host
        self.clients = []
        self.shutdown = False

        self.s.setblocking(0)

        self.lock = threading.Lock()
        self.sendPacket = None
        self.recvPacket = None

        if self.host:
            self.thread = threading.Thread(target = self.runServer)
        else:
            self.thread = threading.Thread(target = self.runClient)
        self.thread.start()

    def runServer(self):
        while True:
            inputs = [self.s] + self.clients
            readable, writable, exceptional = select.select(inputs, [], inputs)
            if self.shutdown:
                return

            if self.s in readable:
                c, addr = self.s.accept()
                c.setblocking(0)
                self.clients.append(c)
                print('new client')
                readable.remove(self.s)

            for c in readable:
                data = c.recv(4096)
                print('recv:', data)
                if not data:
                    self.clients.remove(c)

    def runClient(self):
        recvData = b''
        while True:
            inputs = [self.s]
            readable, writable, exceptional = select.select(inputs, [], inputs)
            if self.shutdown:
                return

            data = self.s.recv(4096)
            if not data:
                print('disconnected from server')
                return

            recvData += data
            if len(recvData) >= 4:
                length = struct.unpack_from('!I', recvData)[0]
                if len(recvData) >= 4 + length:
                    with self.lock:
                        self.recvPacket = recvData[4:4 + length]
                    recvData = recvData[4 + length:]

    def stop(self):
        self.shutdown = True
        self.s.shutdown(socket.SHUT_RD)
        self.thread.join()

    def update(self, gameState):
        if self.host:
            with self.lock:
                data = pickle.dumps(gameState)
                self.sendPacket = struct.pack('!I', len(data)) + data
                for c in self.clients:
                    c.sendall(self.sendPacket)

            return gameState
        else:
            with self.lock:
                if self.recvPacket is not None:
                    return pickle.loads(self.recvPacket)
            return gameState

    def isHost(self):
        return self.host

    def getNumPlayers(self):
        return self.numPlayers
