# -*- coding:utf-8 -*-
import os
import unittest
import time
from server.xmlrpc_services.player.CharacterPersistence import CharacterPersistence
from server.xmlrpc_services.player.PlayerHandlerService import PlayerHandlerService


class TestCharacterPersistence(unittest.TestCase):

    def test_character_creation_and_retrival_returns_correct_area_id(self):
        cp = CharacterPersistence(":memory:")

        character_id, initial_area = cp.create_character(account_id=1, character_name="Sheepy")

        self.assertEqual(cp.INITIAL_AREA, initial_area)

        chars = cp.get_available_characters_for_account(account_id=1)

        self.assertEqual(1, len(chars), "Character count was not 1")

        character_id, name = chars[0]

        self.assertEqual("Sheepy", name)

        self.assertEqual(cp.INITIAL_AREA, cp.get_character_area(account_id=1, character_id=character_id))

    def test_wearing_states_behave_correctly(self):
        cp = CharacterPersistence(":memory:")

        character_id, initial_area = cp.create_character(account_id=1, character_name="Sheepy")

        result = cp.get_wearing_states(character_id)
        self.assertEqual([], result)

        cp.save_wearing_states(character_id, {1: True, 2: True, 4: True}.keys())

        result = cp.get_wearing_states(character_id)
        self.assertEqual([1, 2, 4], result)


class TestItemPersistence(unittest.TestCase):

    def test_area_maximum_id(self):
        if os.path.isfile("test_player.db"):
            os.remove("test_player.db")
        self.item_service = PlayerHandlerService("test_player.db")

        character_id, area_start = self.item_service.create_character(1, "TestCharacter")
        self.item_service.save_player_position(1, character_id, (1, 5, 3))
        time.sleep(0.1)

        char = self.item_service.get_character(character_id)

        self.assertEqual(char['pos_x'], 5)
        self.assertEqual(char['pos_y'], 3)
        self.assertEqual(char['orientation'], 1)
        self.assertEqual(char['character_id'], 1)
        self.assertEqual(char['account_id'], 1)
        self.assertEqual(char['character_name'], "TestCharacter")