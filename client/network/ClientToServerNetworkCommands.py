# -*- coding:utf-8 -*-
from common.constants.ClientPackagePrefixes import ClientPackagePrefixes


class ClientWantsToOpenContainerCommand():

    @staticmethod
    def build_package(container_type):
        return ClientPackagePrefixes.CLIENT_WANTS_OPEN_CONTAINER + str(container_type)

    @staticmethod
    def from_string(string):
        container_type = string
        return int(container_type)


class ClientWantsToCloseContainerCommand():

    @staticmethod
    def build_package(container_type):
        return ClientPackagePrefixes.CLIENT_WANTS_CLOSE_CONTAINER + str(container_type)

    @staticmethod
    def from_string(string):
        container_type = string
        return int(container_type)

class ClientWantsToMoveItem():

    @staticmethod
    def build_package(container_type_from, container_type_to, item_id_source, item_new_start_position):
        return ClientPackagePrefixes.CLIENT_WANTS_TO_MOVE_ITEM + str(container_type_from) + ";" \
                + str(container_type_to) + ";" + str(item_id_source) + ";" + str(item_new_start_position[0]) \
               + ";" + str(item_new_start_position[1])

    @staticmethod
    def from_string(string):
        data = string.split(";")
        container_type_from = int(data[0])
        container_type_to = int(data[1])
        item_id_source = int(data[2])
        item_new_start_pos_x = int(data[3])
        item_new_start_pos_y = int(data[4])
        return container_type_from, container_type_to, item_id_source, (item_new_start_pos_x, item_new_start_pos_y)


class ClientWantsToCraft():

    @staticmethod
    def build_package():
        return ClientPackagePrefixes.CLIENT_WANTS_TO_CRAFT

    @staticmethod
    def from_string(string):
        assert len(string) == 0
        return ""


class ClientSendsFinishedDescriptionOfCraftingResult():

    @staticmethod
    def build_package(item_type_id, text):
        return ClientSendsFinishedDescriptionOfCraftingResult.prefix() + str(item_type_id) + ";" + str(text)

    @staticmethod
    def from_string(string):
        data = string.split(";")
        item_type_id = int(data[0])
        text = str(data[1])
        return item_type_id, text

    @staticmethod
    def prefix():
        return ClientPackagePrefixes.CLIENT_SENDS_FINISHED_DESCRIPTION


class ClientSendsLoginMessage():

    @staticmethod
    def build_package(session_key, account_id, character_id):
        return ClientSendsLoginMessage.prefix() + ";".join([str(session_key), str(account_id), str(character_id)])

    @staticmethod
    def from_string(string):
        data = string.split(";")
        session_key = str(data[0])
        account_id = int(data[1])
        character_id = int(data[2])
        return session_key, account_id, character_id

    @staticmethod
    def prefix():
        return ClientPackagePrefixes.CLIENT_SENDS_LOGIN_MESSAGE

class ClientInteractsForWearingItem():

    @staticmethod
    def build_package(item_uid):
        return ClientInteractsForWearingItem.prefix() + str(item_uid)

    @staticmethod
    def from_string(string):
        return int(string)

    @staticmethod
    def prefix():
        return ClientPackagePrefixes.CLIENT_WANTS_TO_WEAR_ITEM


class ClientWantsToUse():

    @staticmethod
    def build_package():
        return ClientWantsToUse.prefix()

    @staticmethod
    def from_string(string):
        return None

    @staticmethod
    def prefix():
        return ClientPackagePrefixes.CLIENT_WANTS_TO_USE



