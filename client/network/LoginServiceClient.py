import errno
import xmlrpclib
from socket import error as socket_error


class AccountResponse(object):

    NO_ERROR = 0
    DOUBLE_USERNAME = 1
    NETWORK_ERROR = 2
    INCORRECT_CREDENTIALS = 3

    def __init__(self, success, account_id, session_key, available_characters, reason=None, code=0):
        self.success = success
        self.account_id = account_id
        self.session_key = session_key
        self.available_characters = available_characters
        self.reason = reason
        self.code = code

    @staticmethod
    def from_dict(dictionary):
        return AccountResponse(dictionary["success"], dictionary["account_id"],
                                     dictionary["session_key"], dictionary["available_characters"],
                                     dictionary["reason"], dictionary["code"])


class CharacterPayload():

    def __init__(self, character_id, name, description):
        self.character_id = character_id
        self.name = name
        self.description = description

    @staticmethod
    def from_dict(dictionary):
        return CharacterPayload(dictionary["character_id"],
                                dictionary["name"],
                                dictionary["description"])


class CharacterResponse(object):

    NO_TUT_AREA_AVAILABLE = 5
    AREA_OF_PLAYER_IS_NONE = 4
    CANT_CREATE_CHAR = 3
    ACC_IS_NONE = 2
    NO_CONN_INFO = 1

    def __init__(self, success, character_payload, connection_info, is_still_tutorial, reason=None):
        self.success = success
        self.character_payload = character_payload
        self.connection_info = connection_info
        self.is_still_tutorial = is_still_tutorial
        self.reason = reason

    @staticmethod
    def from_dict(dictionary):
        return CharacterResponse(dictionary["success"],
                                 dictionary.get("character_payload", None),
                                 dictionary.get("connection_info", None),
                                 dictionary.get("is_still_tutorial", None),
                                 dictionary.get("reason", None))

    def __repr__(self):
        return "Success: {}, CharPayload: {}, ConnectionInfo: {}, StillTutorial: {}, Reason: {}"\
            .format(self.success, self.character_payload, self.connection_info, self.is_still_tutorial, self.reason)


class LoginServerClient(object):

    def __init__(self, server_host, server_port):
        self.login_server_xmlrpc = xmlrpclib.ServerProxy('http://%s:%s' % (server_host, server_port), allow_none=True)

    def ping(self):
        try:
            return self.login_server_xmlrpc.ping()
        except:
            return False

    def general_login(self, login, password):
        try:
            result = self.login_server_xmlrpc.general_login(login, password)
            return AccountResponse.from_dict(result)
        except socket_error as serr:
            if serr.errno == errno.ECONNREFUSED:
                return AccountResponse(False, code=AccountResponse.NETWORK_ERROR, reason="Service not reachable",
                                    account_id=None, session_key=None, available_characters=None)
            raise serr

    def create_account(self, username, password):
        """ This method is used to request an account creation - it will return the same info
            like when you are logging in the first time without any character
            :param username: The username you wish to use
            :param password: The password for your account
            :return: CreateAccountResponse
        """
        try:
            result = self.login_server_xmlrpc.create_account(username, password)
            create_account_response = AccountResponse.from_dict(result)
            return create_account_response
        except socket_error:
            raise Exception("LoginServerClientError", "Connection Refused!")

    def create_character(self, account_id, session_key):
        try:
            result = self.login_server_xmlrpc.create_character(account_id, session_key)
            character_response = CharacterResponse.from_dict(result)
            return character_response
        except socket_error:
            raise Exception("LoginServerClientError", "Connection Refused!")

    def login_character(self, account_id, session_key, char_id_chosen):
        try:
            result = self.login_server_xmlrpc.login_character(account_id, session_key, char_id_chosen)
            character_response = CharacterResponse.from_dict(result)
            return character_response
        except socket_error:
            raise Exception("LoginServerClientError", "Connection Refused!")