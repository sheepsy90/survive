from client.logic.WearingManager import WearingManager
from client.level.client_level_loader import load_level_for_client
from common.constants.ScriptingConstants import ScriptingConstants


class UsingHistory(object):

    def __init__(self, sound_engine):
        self.sound_engine = sound_engine
        self.using_history_list = []

    def add_using_entry(self, using_result):

        if using_result == ScriptingConstants.ID_CARD_REQUIRED:
            self.sound_engine.play("id_card_required")
        elif using_result == ScriptingConstants.NOT_AUTHORIZED:
            self.sound_engine.play("not_authorized")
        elif using_result == ScriptingConstants.DOOR_OPENED:
            self.sound_engine.play("access_granted")
        self.using_history_list.append(using_result)

    def has_entry_in_history(self, entry):
        return entry in self.using_history_list



class ClientLevelManager():

    def __init__(self, sound_system):
        self.client_level = None

        # The Logic Objects that are Necessary
        self.wearing_manager = WearingManager()
        self.using_history = UsingHistory(sound_system)
        self.general_item_watcher = {}

    def set_level_identifier(self, level_identifier):
        """ This method is responsible for loading a specific level by the client based on the identifier
            given - furthermore it can control to delete all knowledge about the last level """
        self.client_level = load_level_for_client(level_identifier)

    def get_current_level(self):
        return self.client_level

    def get_wearing_manager(self):
        return self.wearing_manager

    def get_using_history(self):
        return self.using_history

    def get_general_item_watcher(self):
        return self.general_item_watcher




