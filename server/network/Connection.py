import time
from common.helper import send_message


class Connection(object):

    def __init__(self, addr):
        self.addr = addr
        self.last_interaction = time.time()

    def update_last_interaction(self):
        self.last_interaction = time.time()

    def get_time_since_last_ttl(self):
        return time.time() - self.last_interaction

    def __str__(self):
        return str(self.addr) + " - " + str(self.last_interaction)

    def send_rejection(self, sock):
        send_message(sock, 'RJC', self.addr)