# -*- coding:utf-8 -*-
import xmlrpclib
from server.configuration.configuration import Configuration


class ArgumentMemorizerAndCascadeCallDecorator(object):

    def __init__(self, key_size, value_size):
        self.key_size = key_size
        self.value_size = value_size

        self.memorize_dictionary = {}

    def __call__(self, f):

        def wrapped_f(*args):
            args_without_self = args[1:]
            assert len(args_without_self) == self.key_size + self.value_size, (args_without_self, self.key_size, self.value_size)

            sub_dict = self.memorize_dictionary
            for e in args_without_self[0:self.key_size]:
                if e in sub_dict:
                    sub_dict = sub_dict[e]
                else:
                    sub_dict = None
                    break

            values = args_without_self[self.key_size:]

            if sub_dict is None:

                # Enter it inti subdict and call the function
                sub_dict = self.memorize_dictionary
                for e in args_without_self[0:self.key_size]:
                    if e not in sub_dict:
                        sub_dict[e] = {}
                    sub_dict = sub_dict[e]

                sub_dict["data"] = str(values)

                f(*args)
            else:
                data = sub_dict["data"]

                if data != str(values):
                    sub_dict["data"] = str(values)

                    f(*args)

        return wrapped_f

class PlayerHandlerServiceClient():
    """ This class lives within a game server instance and can talks to the Character Persistence """

    def __init__(self):
        config = Configuration()
        host, port = config.get_configuration()["PlayerHandlerServiceXMLRPC"]
        self.player_service = xmlrpclib.ServerProxy('http://%s:%s' % (str(host), str(port)), allow_none=True)

    def load_characters_for_account(self, account_id):
        return self.player_service.load_character_list(account_id)

    def create_character(self, account_id, name):
        return self.player_service.create_character(account_id, name)

    def get_area_for_character(self, account_id, character_id):
        return self.player_service.get_character_area(account_id, character_id)

    def set_session_key_for_account(self, account_id, session_key):
        return self.player_service.set_session_key_for_account(account_id, session_key)

    def get_session_key_for_account(self, account_id):
        return self.player_service.get_session_key_for_account(account_id)

    def get_character(self, character_id):
        return self.player_service.get_character(character_id)

    def set_character_to_new_area(self, account_id, character_id, new_area_id, start_position):
        return self.player_service.set_character_to_new_area(account_id, character_id, new_area_id, start_position)

    def can_create_character(self, account_id):
        return self.player_service.can_create_character(account_id)

    def get_player_health_modifiers(self, character_id):
        return self.player_service.get_player_health_modifiers(character_id)

    def get_wearing_states(self, character_id):
        return self.player_service.get_wearing_states(character_id)

    @ArgumentMemorizerAndCascadeCallDecorator(key_size=2, value_size=1)
    def save_player_position(self, account_id, character_id, discrete_position):
        # TODO - check for change and only call service when changes occured
        return self.player_service.save_player_position(account_id, character_id, discrete_position)

    @ArgumentMemorizerAndCascadeCallDecorator(key_size=1, value_size=2)
    def save_backpack_content(self, character_id, content, item_root_positions):
        prepared = {}
        for key in content:
            item = content[key]
            start_pos = item_root_positions[key]
            id = item.get_id()
            prepared[str(id)] = start_pos

        return self.player_service.save_backpack_content(character_id, prepared)

    @ArgumentMemorizerAndCascadeCallDecorator(key_size=1, value_size=1)
    def save_health_modifiers(self, character_id, modifier_dict):
        transformed_to_list = [[key, modifier_dict[key]] for key in modifier_dict]
        return self.player_service.save_health_modifiers(character_id, transformed_to_list)

    @ArgumentMemorizerAndCascadeCallDecorator(key_size=1, value_size=1)
    def save_wearing_states(self, character_id, wearing_states):
        return self.player_service.save_wearing_states(character_id, wearing_states)

    @ArgumentMemorizerAndCascadeCallDecorator(key_size=1, value_size=1)
    def save_tutorial_state(self, character_id, tutorial_state):
        return self.player_service.save_tutorial_state(character_id, tutorial_state)

    def get_backpack_size_for_character(self, character_id):
        return self.player_service.get_backpack_size_for_character(character_id)

    def get_backpack_items_for_character(self, character_id):
        return self.player_service.get_backpack_items_for_character(character_id)