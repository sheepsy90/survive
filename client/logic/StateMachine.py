import time


class StateMachine(object):

    def __init__(self):
        self.is_connected = False
        self.last_ttl_timestamp = time.time()
        self.session_key = None
        self.account_id = None
        self.character_id = None
        self.tutorial = None
        self.last_time_heard_from_server = None

    def is_not_connected(self):
        return not self.is_connected

    def set_connected(self, value):
        self.is_connected = value

    def last_time_ttl(self):
        return self.last_ttl_timestamp

    def refresh_last_time_ttl(self):
        self.last_ttl_timestamp = time.time()

    def update_time_heard_from_server(self):
        self.last_time_heard_from_server = time.time()

    def is_last_time_heard_from_server_longer_than(self, delta):
        if self.last_time_heard_from_server is not None and (time.time() - self.last_time_heard_from_server) > delta:
            return True
        return False

    def set_session_key(self, session_key):
        self.session_key = session_key

    def get_session_key(self):
        return self.session_key

    def set_account_id(self, account_id):
        self.account_id = account_id

    def set_character_id(self, character_id):
        self.character_id = character_id

    def set_character_is_still_tutorial(self, value):
        self.tutorial = value

    def is_character_still_tutorial(self):
        return self.tutorial

    def get_account_id(self):
        return self.account_id

    def get_character_id(self):
        return self.character_id