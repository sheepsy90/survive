# -*- coding:utf-8 -*-


class Account(object):

    def __init__(self, id, login, password, session_key):
        self.id = id
        self.login = login
        self.password = password
        self.session_key = session_key

    def get_id(self):
        return self.id

    def get_login(self):
        return self.login

    def is_correct_password(self, entered_pw):
        return entered_pw == self.password

    def is_correct_session_key(self, entered_session_key):
        return self.session_key == entered_session_key

    def set_session_key(self, key):
        self.session_key = key

    def get_session_key(self):
        return self.session_key