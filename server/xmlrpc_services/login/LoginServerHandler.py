# -*- coding:utf-8 -*-
import logging
import random
import unittest
import uuid

from client.network.LoginServiceClient import AccountResponse, CharacterResponse, CharacterPayload

from server.xmlrpc_services.gameservermanager.GameServerManagerClient import GameServerManagerClient
from server.xmlrpc_services.login.AccountPersistence import AccountPersistence
from server.xmlrpc_services.player.PlayerHandlerServiceClient import PlayerHandlerServiceClient

logger = logging.getLogger(__name__)


class LoginServerHandler(object):
    def __init__(self, db_path="accounts.db"):

        self.persistence = AccountPersistence(db_path)

        self.game_server_manager_client = GameServerManagerClient()
        self.player_handler_service_client = PlayerHandlerServiceClient()

    def general_login(self, username, password):

        account = self.persistence.load_account_by_name(username)

        # If we don't know the username don't allow any further things
        if account is None:
            print "[LOGIN] Invalid username"
            return AccountResponse(False, None, None, None, reason="Incorrect Credentials",
                                   code=AccountResponse.INCORRECT_CREDENTIALS)

        # If passwords don't match don't allow further things
        if not account.is_correct_password(password):
            print "[LOGIN] Invalid password"
            return AccountResponse(False, None, None, None, reason="Incorrect Credentials",
                                   code=AccountResponse.INCORRECT_CREDENTIALS)

        available_characters = self.player_handler_service_client.load_characters_for_account(account.get_id())

        # Generate random session key to make sure that the user don't need his name and pw all the time
        random_session_key = str(uuid.uuid4())

        logger.info("Available Characters are: {}".format(available_characters))

        character_payload_list = [CharacterPayload(e[0], e[1], "custom description") for e in available_characters]

        self.persistence.set_session_key_for_account(account.get_id(), random_session_key)

        return AccountResponse(True, account.get_id(), random_session_key, character_payload_list)

    def verify_and_get_account(self, account_id, session_key):

        account = self.persistence.load_account_by_id(account_id)

        if account is None:
            logger.warn("[LOGIN] Account Id not available {}".format(account_id))
            return None

        if not account.is_correct_session_key(session_key):
            logger.warn("[LOGIN]  Account Session Key not valid - given {} but should be {}"
                        .format(session_key, account.get_session_key()))
            return None

        return account

    def create_character(self, account_id, session_key):
        """ Create a character by
        :param account_id: The account id of the user
        :param session_key: The session key received by general login
        :return: connection_info as to which server to connect next
        """
        logger.info("Account {} requested new character".format(account_id))
        names = ["Jessy", "Misty", "Sara", "Melanie", "Kara"]
        random.shuffle(names)
        name = names[0]

        account = self.verify_and_get_account(account_id, session_key)

        if account is None:
            logger.warn("Account is None for id {} and session_key {}".format(account_id, session_key))
            return CharacterResponse.from_dict({"success": False, "reason": CharacterResponse.ACC_IS_NONE})

        if not self.player_handler_service_client.can_create_character(account_id):
            logger.warn("Can't create character for account id {} and session_key {}".format(account_id, session_key))
            return CharacterResponse.from_dict({"success": False, "reason": CharacterResponse.CANT_CREATE_CHAR})

        character_id, area_of_player = self.player_handler_service_client.create_character(account_id, name)
        character = self.player_handler_service_client.get_character(character_id)

        is_still_tutorial = self.is_player_still_in_tutorial(character)

        # Set the session key for the user within the player xmlrpc service
        self.player_handler_service_client.set_session_key_for_account(account_id, session_key)

        character_payload = CharacterPayload(character_id, name, "custom description")

        return CharacterResponse(True, character_payload, None, is_still_tutorial)

    def login_character(self, account_id, session_key, character_id):
        account = self.verify_and_get_account(account_id, session_key)

        if account is None:
            logger.warn("Account is None for id {} and session_key {}".format(account_id, session_key))
            return CharacterResponse.from_dict({"success": False, "reason": CharacterResponse.ACC_IS_NONE})

        character = self.player_handler_service_client.get_character(character_id)
        area_of_player = character["area_id"]

        if area_of_player is None:
            logger.error("Couldn't retrieve area for player {} with character_id {} and area {}"
                         .format(account_id, character_id, area_of_player))
            return CharacterResponse.from_dict({"success": False, "reason": CharacterResponse.AREA_OF_PLAYER_IS_NONE})

        is_still_tutorial = self.is_player_still_in_tutorial(character)
        connection_info = self.game_server_manager_client.get_game_service_for_area(is_still_tutorial, area_of_player)

        if connection_info is None:
            if is_still_tutorial:
                logger.warn("Couldn't retrieve connection info - no open tutorial areas!"
                            .format(account_id, area_of_player))
                return CharacterResponse.from_dict({"success": False, "reason": CharacterResponse.NO_TUT_AREA_AVAILABLE})
            else:
                logger.error("Couldn't retrieve connection info for id {} area {}. Seems to be no such area!"
                             .format(account_id, area_of_player))
                return CharacterResponse.from_dict({"success": False, "reason": CharacterResponse.NO_CONN_INFO})

        self.player_handler_service_client.set_session_key_for_account(account_id, session_key)

        return CharacterResponse.from_dict({"success": True,
                                            "connection_info": connection_info,
                                            "is_still_tutorial": is_still_tutorial})

    @staticmethod
    def is_player_still_in_tutorial(character):
        return int(character["tutorial_state"]) == 1

    def create_account(self, username, password):
        has_username = self.persistence.has_username(username)

        if has_username:
            # The wished username is already taken
            return AccountResponse(False, None, None, None, reason="Username already exists",
                                   code=AccountResponse.DOUBLE_USERNAME)
        else:
            # Account can be created
            self.persistence.create_account(username, password)
            return self.general_login(username, password)


