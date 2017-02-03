# -*- coding:utf-8 -*-
import time
from client.network import ClientToServerNetworkCommands
from client.network.ClientToServerNetworkCommands import ClientWantsToMoveItem, ClientWantsToCraft, \
    ClientSendsFinishedDescriptionOfCraftingResult, ClientSendsLoginMessage, ClientInteractsForWearingItem, \
    ClientWantsToUse
from common.constants.ClientPackagePrefixes import ClientPackagePrefixes
from common.constants.ContainerConstants import ContainerConstants

from common.helper import send_message


class ClientSocketWrapper():

    def __init__(self, socket, ip, port):
        self.socket = socket
        self.ip = ip
        self.port = port

        self.last_time_wearing_interaction = 0
        self.last_time_moving_command = 0

    def send_message(self, message):
        send_message(self.socket, message, (self.ip, self.port))

    def set_new_connection_info(self, new_ip, new_port):
        self.ip = new_ip
        self.port = new_port

    def send_close_backpack_command(self):
        self.send_message(ClientToServerNetworkCommands.ClientWantsToCloseContainerCommand.build_package(ContainerConstants.CONTAINER_TYPE_BACKPACK))

    def send_open_backpack_command(self):
        self.send_message(ClientToServerNetworkCommands.ClientWantsToOpenContainerCommand.build_package(ContainerConstants.CONTAINER_TYPE_BACKPACK))

    def send_open_normal_loot_container_command(self):
        self.send_message(ClientToServerNetworkCommands.ClientWantsToOpenContainerCommand.build_package(ContainerConstants.CONTAINER_TYPE_NORMAL))

    def send_close_normal_loot_container_command(self):
        self.send_message(ClientToServerNetworkCommands.ClientWantsToCloseContainerCommand.build_package(ContainerConstants.CONTAINER_TYPE_NORMAL))

    def send_open_crafting_container_command(self):
        self.send_message(ClientToServerNetworkCommands.ClientWantsToOpenContainerCommand.build_package(ContainerConstants.CONTAINER_TYPE_CRAFTING))

    def send_close_crafting_container_command(self):
        self.send_message(ClientToServerNetworkCommands.ClientWantsToCloseContainerCommand.build_package(ContainerConstants.CONTAINER_TYPE_CRAFTING))

    def send_moving_item_request(self, container_type_from, container_type_to, item_id_source, item_new_start_position):
        self.send_message(ClientWantsToMoveItem.build_package(container_type_from, container_type_to, item_id_source, item_new_start_position))

    def send_crafting_request(self):
        self.send_message(ClientWantsToCraft.build_package())

    def send_item_type_description(self, item_type_id, text):
        self.send_message(ClientSendsFinishedDescriptionOfCraftingResult.build_package(item_type_id, text))

    def send_login_message_to_game_server(self, session_key, account_id, character_id):
        self.send_message(ClientSendsLoginMessage.build_package(session_key, account_id, character_id))

    def send_movment_request(self, direction):
        if time.time() - self.last_time_moving_command > 0.05:
            self.send_message(ClientPackagePrefixes.CLIENT_WANTS_TO_MOVE+'%i;%i' % (direction[0], direction[1]))
            self.last_time_moving_command = time.time()

    def send_client_requests_wearing_item(self, item_uid):
        if time.time() - self.last_time_wearing_interaction > 0.2:
            self.last_time_wearing_interaction = time.time()
            self.send_message(ClientInteractsForWearingItem.build_package(item_uid))

    def send_client_wants_to_use(self):
        self.send_message(ClientWantsToUse.build_package())
