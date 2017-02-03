from server.network.Connection import Connection

class ConnectionHandler():

    def __init__(self):
        self.connections = {}

    def has_connection(self, addr):
        return addr in self.connections.keys()

    def get_connection(self, addr):
        return self.connections[addr]

    def add_connection(self, addr):
        c = Connection(addr)
        self.connections[addr] = c
        return c

    def del_connection(self, addr):
        del self.connections[addr]