import socket
import select
import threading

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

        if self.host:
            self.thread = threading.Thread(target = self.runServer)
        else:
            self.thread = threading.Thread(target = self.runClient)
        self.thread.start()

    def runServer(self):
        while True:
            readable, writable, exceptional = select.select([self.s] + self.clients, [], [])
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
        while True:
            readable, writable, exceptional = select.select([self.s], [], [])
            if self.shutdown:
                return

            data = self.s.recv(4096)
            print('recv:', data)

    def stop(self):
        self.shutdown = True
        self.s.shutdown(socket.SHUT_RDWR)

    def update(self):
        pass

    def isHost(self):
        return self.host

    def getNumPlayers(self):
        return self.numPlayers
