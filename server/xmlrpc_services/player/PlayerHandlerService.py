from multiprocessing import Queue
import os
import threading
import unittest
import time
from server.xmlrpc_services.player.CharacterPersistence import CharacterPersistence


class PlayerServiceSQLQueueCommand():

    UPDATE_TUTORIAL_STATE = 6
    SAVE_WEARING_STATES = 5
    SAVE_HEALTH_MODIFIERS = 4
    SAVE_POSITION = 1
    SAVE_BACKPACK_CONTENT = 3

    def __init__(self, type, data):
        self.type = type
        self.data = data



class PlayerHandlerService(threading.Thread):

    def __init__(self, db_name="players.db"):
        threading.Thread.__init__(self)
        self.daemon = True

        self.db_name = db_name

        self.persistence = CharacterPersistence(db_name)
        self.session_keys = {}

        self.player_saving_queue = Queue()

        self.start()

    def load_character_list(self, account_id):
        return self.persistence.get_available_characters_for_account(account_id)

    def create_character(self, account_id, name):
        character_id, area_id = self.persistence.create_character(account_id, name)
        return character_id, area_id

    def get_character_area(self, account_id, character_id):
        area_id = self.persistence.get_character_area(account_id, character_id)

        return area_id

    def set_session_key_for_account(self, account_id, session_key):
        self.session_keys[account_id] = session_key

    def get_session_key_for_account(self, account_id):
        if account_id in self.session_keys:
            return self.session_keys[account_id]

    def get_character(self, character_id):
        return self.persistence.get_character(character_id)

    def set_character_to_new_area(self, account_id, character_id, new_area_id, start_position):
        return self.persistence.set_character_to_new_area(account_id, character_id, new_area_id, start_position)

    def can_create_character(self, account_id):
        return self.persistence.can_create_character(account_id)

    def get_backpack_size_for_character(self, character_id):
        return self.persistence.get_backpack_size_for_character(character_id)

    def get_player_health_modifiers(self, character_id):
        return self.persistence.get_player_health_modifiers(character_id)

    def get_backpack_items_for_character(self, character_id):
        return self.persistence.get_backpack_items_for_character(character_id)

    def get_wearing_states(self, character_id):
        return self.persistence.get_wearing_states(character_id)

    def save_player_position(self, account_id, character_id, discrete_position):
        return self.player_saving_queue.put(PlayerServiceSQLQueueCommand(
                                            PlayerServiceSQLQueueCommand.SAVE_POSITION,
                                            [account_id, character_id, discrete_position]))

    def save_backpack_content(self, character_id, prepared_info):
        return self.player_saving_queue.put(PlayerServiceSQLQueueCommand(
                                    PlayerServiceSQLQueueCommand.SAVE_BACKPACK_CONTENT,
                                    [character_id, prepared_info]))

    def save_health_modifiers(self, character_id, modifier_dict):
        return self.player_saving_queue.put(PlayerServiceSQLQueueCommand(
                                    PlayerServiceSQLQueueCommand.SAVE_HEALTH_MODIFIERS,
                                    [character_id, modifier_dict]))

    def save_wearing_states(self, character_id, wearing_states):
        return self.player_saving_queue.put(PlayerServiceSQLQueueCommand(
                                    PlayerServiceSQLQueueCommand.SAVE_WEARING_STATES,
                                    [character_id, wearing_states]))

    def save_tutorial_state(self, character_id, tutorial_state):
        return self.player_saving_queue.put(PlayerServiceSQLQueueCommand(
                                    PlayerServiceSQLQueueCommand.UPDATE_TUTORIAL_STATE,
                                    [character_id, tutorial_state]))

    def run(self):
        persistence = CharacterPersistence(self.db_name)

        while True:
            pssqlqc = self.player_saving_queue.get()

            if pssqlqc.type == PlayerServiceSQLQueueCommand.SAVE_POSITION:
                account_id, character_id, discrete_position = pssqlqc.data
                persistence.save_player_position(account_id, character_id, discrete_position)
            elif pssqlqc.type == PlayerServiceSQLQueueCommand.SAVE_BACKPACK_CONTENT:
                character_id, prepared_info = pssqlqc.data
                persistence.save_backpack_items(character_id, prepared_info)
            elif pssqlqc.type == PlayerServiceSQLQueueCommand.SAVE_HEALTH_MODIFIERS:
                character_id, modifier = pssqlqc.data
                persistence.save_health_modifiers(character_id, modifier)
            elif pssqlqc.type == PlayerServiceSQLQueueCommand.SAVE_WEARING_STATES:
                character_id, wearing_states = pssqlqc.data
                persistence.save_wearing_states(character_id, wearing_states)
            elif pssqlqc.type == PlayerServiceSQLQueueCommand.UPDATE_TUTORIAL_STATE:
                character_id, tutorial_state = pssqlqc.data
                persistence.save_tutorial_state(character_id, tutorial_state)

            time.sleep(0.01)


