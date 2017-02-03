# -*- coding:utf-8 -*-
import logging

from client.network.ClientToServerNetworkCommands import ClientSendsLoginMessage
from common.helper import extract_data_package
from server.character_representations.CharacterWearingHandler import CharacterWearingHandler
from server.character_representations.OnlinePlayer import OnlinePlayer
from server.health_modifier.OverTimeEffectModifiers import HungerOverTimeEffect
from server.xmlrpc_services.items.Item import Item


logger = logging.getLogger(__name__)


class OnlinePlayerLoader():
    """ This class is responsible for loading a new player when a ClientSendsLoginMessage arrives """

    FULL_DATA_PROPAGATION = "FDP"

    def __init__(self, area_id, connection_handler, server_command_wrapper, players_service_client,
                 crafting_service_client, item_service_client, online_player_system, container_state_mem_system):
        self.area_id = area_id
        self.connection_handler = connection_handler
        self.server_command_wrapper = server_command_wrapper

        self.online_player_system = online_player_system

        self.players_service_client = players_service_client
        self.crafting_service_client = crafting_service_client
        self.item_service_client = item_service_client

        self.container_state_mem_system = container_state_mem_system

    def create_new_player(self, addr, data):
        """ This method is responsible for the first interaction with a client when he is trying
            to log in on this game_server_instance """

        command, payload = extract_data_package(data)

        # First create a new connection to be able to use the rejection mechanics
        connection = self.connection_handler.add_connection(addr)

        # If it is not a login command reject the request and remove it from the connection_handler
        if command != ClientSendsLoginMessage.prefix():
            logger.error("Client was supposed to send a login package first, but got: {}".format(data))
            self.server_command_wrapper.send_rejection(connection)
            self.connection_handler.del_connection(addr)
            return

        session_key, account_id, character_id = ClientSendsLoginMessage.from_string(payload)
        print session_key, account_id, character_id

        # Get the session_key from the service and if it don't match by the given one reject the user
        session_key_from_service = self.players_service_client.get_session_key_for_account(account_id)

        if session_key_from_service != session_key:
            logger.error("Session Key is not valid for acc {} and char {}".format(account_id, character_id))
            self.server_command_wrapper.send_rejection(connection)
            self.connection_handler.del_connection(addr)
            return

        # Get the Character information - build up everything and integrate the player to the system
        character_data = self.players_service_client.get_character(character_id)

        if character_data is None:
            logger.error("Could not load character data - was None for - acc_id {} char_id {}"
                         .format(account_id, character_id))
            self.server_command_wrapper.send_rejection(connection)
            return

        # Otherwise check if the player is logged in on the correct area handler
        player_area = character_data.get("area_id", None)

        if player_area != self.area_id:
            logger.error("This instance doesn't handle the area the character has. Was {} but handling only {}"
                         .format(player_area, self.area_id))
            self.server_command_wrapper.send_rejection(connection)
            self.connection_handler.del_connection(addr)
            return

        # If all is correct we start creating the player
        return self.really_create_player(character_data, connection)

    @staticmethod
    def extract_character_info(character_data):
        position = character_data["orientation"], character_data["pos_x"], character_data["pos_y"]
        account_id = character_data["account_id"]
        character_id = character_data["character_id"]
        tutorial_state = character_data["tutorial_state"]
        character_name = character_data["character_name"]
        return account_id, character_id, character_name, position, tutorial_state

    def load_and_add_health_modifiers(self, player):
        character_id = player.get_character_id()
        mods = self.players_service_client.get_player_health_modifiers(character_id)
        if mods is not None:
            health_modifier = player.get_health_modifier_component()
            for element in mods:
                type, amount = element
                health_modifier.set_modifier(type, amount)

            # Set the modifiers that are shadowed for the user every time
            health_modifier.set_modifier(HungerOverTimeEffect.TYPE_ID, 1)

    def create_wearing_handler_for_player(self, player):
        character_id = player.get_character_id()
        wearing_states = self.players_service_client.get_wearing_states(character_id)
        cwh = CharacterWearingHandler(self.crafting_service_client)

        for item_id in wearing_states:
            item_info = self.item_service_client.get_item(item_id)
            id, type_id, usages_left = item_info
            item_template = self.crafting_service_client.get_item_template(type_id)
            item = Item(item_template, id, usages_left)
            if not cwh.try_wearing_item(item):
                logger.error("Player {} could not wear item - this should be possible on loading char though!")
                raise ValueError("Try Wearing Item should not return False on loading character")
        player.set_character_wearing_handler(cwh)

    def prepare_inventory(self, player):
        """ This method prepares the backpack container and loads all the items necessary into it.
        :param player: The player to perform this for
        :return:
        """
        character_id = player.get_character_id()
        backpack_size = self.players_service_client.get_backpack_size_for_character(character_id)
        xs, ys = backpack_size
        items_in_backpack = self.players_service_client.get_backpack_items_for_character(character_id)
        container = player.get_inventory()
        container.set_shape(xs, ys)
        # Put all items back to backpack
        for element in items_in_backpack:
            id, sx, sy = element
            item_info = self.item_service_client.get_item(id)
            id, type_id, usages_left = item_info
            item_template = self.crafting_service_client.get_item_template(type_id)
            item = Item(item_template, id, usages_left)
            container.content[id] = item
            container.item_root_positions[id] = (sx, sy)
        container.build_matrix_mapping()
        # Make sure there are no open containers so the client don't runs into problems
        # TODO this is a quick fix
        self.container_state_mem_system.remove_all_open_containers_for_player(player)

    def really_create_player(self, character_data, connection):
        """ This method is necessary to really load the OnlinePlayer Object and all stuff that
            is necessary too for the player to be able to function correctly.
            :param character_data:
            :param connection:
            :return:
        """

        try:
            account_id, character_id, character_name, position, tutorial_state = self.extract_character_info(character_data)
            logger.info("Loading Character with following data: {}".format(character_data))
        except KeyError:
            logger.error("Could not extract all information necessary - from character_data: {}".format(character_data))
            return False

        # Create a new player object
        player = OnlinePlayer(account_id, character_id, character_name, tutorial_state, connection, {'pos': position})

        # Load all the health modifiers from the database
        self.load_and_add_health_modifiers(player)

        # Make sure the wearings are set correctly
        try:
            self.create_wearing_handler_for_player(player)
        except ValueError as e:
            logger.error(str(e))
            return False

        # This method is responsible for loading the backpack size and the items in inventory
        self.prepare_inventory(player)

        # Add the player to the local player service
        self.online_player_system.add_online_player(player)

        # Issue the FullDataPropagation Command to make sure the client gets a fresh set of level information
        player.add_command(OnlinePlayerLoader.FULL_DATA_PROPAGATION, None)