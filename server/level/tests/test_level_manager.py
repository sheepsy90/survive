# -*- coding:utf-8 -*-

import os
import unittest

from server.level.server_level_loader import load_level_for_server


class TestLevelManager(unittest.TestCase):

    __name__ = "TestLevelManager"

    @unittest.skip
    def test_tutorial_load_for_server(self):
        load_level_for_server(os.path.abspath("../../resources/levels/level_tutorial.json"))

    @unittest.skip
    def test_level_after_tutorial_load_for_server(self):
        full_server_level = load_level_for_server(os.path.abspath("../../resources/levels/after_tutorial_level.json"))

        object_id_counter_before = full_server_level.get_world_object_manager().object_id_counter

        world_object = full_server_level.get_world_object_manager().create_world_object(1, 1)

        self.assertEqual(object_id_counter_before+1, world_object.get_object_id())

    @unittest.skip
    def test_level_loading_correctly(self):
        server_level = load_level_for_server(os.path.abspath("../../resources/levels/level_01_left.json"))
        server_level = load_level_for_server(os.path.abspath("../../resources/levels/level_02_right.json"))

    def check_guard(self, server_level, mx, my, guard_level, guard_type):
        walkable_result = server_level.is_walkable(mx, my)

        self.assertFalse(walkable_result.is_walkable)
        self.assertEqual("guard", walkable_result.walking_blocked_type)

        npc_component = walkable_result.additional_information
        self.assertEqual(guard_level, npc_component.get_guard_level())
        self.assertEqual(guard_type, npc_component.get_guard_type())

    def check_guard_is_collidable(self, server_level, mx, my):
        walkable_result = server_level.is_walkable(mx, my)

        self.assertFalse(walkable_result.is_walkable)
        self.assertEqual("collidable", walkable_result.walking_blocked_type)
        payload = walkable_result.additional_information

        self.assertEqual(None, payload)

    @unittest.skip
    def test_first_puzzle_room_works(self):
        """ This is the test for the common area level - when querying the standard objects it should result always
            with the correct values - this is necessary such that this level works as intended. Especially the
            guards and objects that are placed need to be verified.
        """
        # Load the server level - This should work without an error
        server_level = load_level_for_server(os.path.abspath("../../resources/levels/first_puzzle_test.json"))


    def test_two_player_puzzle(self):
        """ This is the test for the common area level - when querying the standard objects it should result always
            with the correct values - this is necessary such that this level works as intended. Especially the
            guards and objects that are placed need to be verified.
        """
        # Load the server level - This should work without an error
        server_level = load_level_for_server(os.path.abspath("../../resources/levels/two_player_puzzle.json"))


    def test_common_room_works_as_expected(self):
        """ This is the test for the common area level - when querying the standard objects it should result always
            with the correct values - this is necessary such that this level works as intended. Especially the
            guards and objects that are placed need to be verified.
        """

        # Load the server level - This should work without an error
        server_level = load_level_for_server(os.path.abspath("../../resources/levels/common_room.json"))

        # Check the NPC - Positions
        self.check_guard(server_level, mx=15, my=35, guard_level=1, guard_type="security")
        self.check_guard(server_level, mx=15, my=27, guard_level=2, guard_type="security")
        self.check_guard(server_level, mx=15, my=13, guard_level=3, guard_type="security")

        self.check_guard_is_collidable(server_level, mx=14, my=35)
        self.check_guard_is_collidable(server_level, mx=14, my=27)
        self.check_guard_is_collidable(server_level, mx=14, my=13)

        self.check_guard(server_level, mx=5, my=35, guard_level=1, guard_type="administration")
        self.check_guard(server_level, mx=5, my=27, guard_level=2, guard_type="administration")
        self.check_guard(server_level, mx=5, my=13, guard_level=3, guard_type="administration")

        self.check_guard_is_collidable(server_level, mx=6, my=35)
        self.check_guard_is_collidable(server_level, mx=6, my=27)
        self.check_guard_is_collidable(server_level, mx=6, my=13)

        walking_result = server_level.is_walkable(i=-1, j=-1)
        self.assertFalse(walking_result.is_walkable)
        self.assertEqual("bounds", walking_result.walking_blocked_type)
        self.assertEqual(None, walking_result.additional_information)

        walking_result = server_level.is_walkable(i=1, j=1)
        self.assertFalse(walking_result.is_walkable)
        self.assertEqual("default", walking_result.walking_blocked_type)
        self.assertEqual(None, walking_result.additional_information)

        walking_result = server_level.is_walkable(i=2, j=2)
        self.assertTrue(walking_result.is_walkable)
        self.assertEqual(None, walking_result.walking_blocked_type)
        self.assertEqual(None, walking_result.additional_information)