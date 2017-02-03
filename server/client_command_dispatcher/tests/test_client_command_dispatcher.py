# -*- coding:utf-8 -*-
"""

^^^^^^^^^^^^

.. moduleauthor:: sheepy <sheepy@informatik.uni-hamburg.de>

History:
* 06.02.15: Created (sheepy)

"""
import unittest

import mock

from common.named_tuples import WalkableResult, NpcComponentProperties
from server.client_command_dispatcher.ClientCommandDispatcher import ClientCommandDispatcher
from server.constants.constans import SRV_NO_MOVED, GUARD_DENYS, GUARD_ALLOWS, AREA_CHANGE, SRV_MOVED, \
    SRV_NO_MOVED_OPEN_CONTAINER, SRV_NO_MOVED_ALREADY_MOVING
from server.world_objects.object_components.NpcComponent import NpcComponent


class TestClientCommandDispatcher(unittest.TestCase):

    def prepare_player_mock(self, is_moving, position):
        moving_component = mock.MagicMock()
        moving_component.is_moving = mock.Mock(return_value=is_moving)
        moving_component.get_discrete_position = mock.Mock(return_value=position)
        player = mock.MagicMock()
        player.get_moving_component = mock.Mock(return_value=moving_component)
        return player

    def prepare_container_mem_mock(self, has_open_container):
        open_container_memorizer = mock.Mock()
        open_container_memorizer.has_open_container = mock.Mock(return_value=has_open_container)
        return open_container_memorizer

    def prepare_server_level_mock(self, is_walkable_result, is_change_area_spot):
        server_level = mock.Mock()
        server_level.is_walkable = mock.Mock(return_value=is_walkable_result)
        server_level.is_change_area_spot = mock.Mock(return_value=is_change_area_spot)
        return server_level

    def prepare_npc_component(self, npc_guard_type, npc_guard_level):
        npc_component = NpcComponent(NpcComponentProperties(npc_type=0,
                                                   is_guard=True,
                                                   npc_guard_type=npc_guard_type,
                                                   npc_guard_orientation="left",
                                                   npc_guard_level=npc_guard_level))
        parent_mock = mock.Mock()
        parent_mock.get_object_id = mock.Mock(return_value=1)
        npc_component.set_parent(parent_mock)
        return npc_component


    def test_guard_allows_to_pass_on_right_card(self):
        server_command_wrapper_mock = mock.Mock()

        client_command_dispatcher = ClientCommandDispatcher(server_command_wrapper_mock)

        player_mock = self.prepare_player_mock(False, (4, 10, 10))
        open_container_mem_mock = self.prepare_container_mem_mock(False)
        npc_component = self.prepare_npc_component("security", 1)
        server_level_mock = self.prepare_server_level_mock(
            is_walkable_result=WalkableResult(is_walkable=False,
                                              walking_blocked_type="guard",
                                              additional_information=npc_component),
            is_change_area_spot=False)

        player_service_client_mock = mock.Mock()
        player_service_client_mock.register_moving_player = mock.Mock()

        player_mock.get_inventory = mock.Mock()
        player_mock.get_inventory().has_sufficient_id_card = mock.Mock(return_value=True)

        result = client_command_dispatcher.handle_player_movement(server_level_mock,
                                                                  player_service_client_mock,
                                                                  player_mock,
                                                                  open_container_mem_mock,
                                                                  "1;0")

        player_mock.get_moving_component().start_moving.assert_called_with((1, 11, 10))
        player_service_client_mock.register_moving_player.assert_called_with(player_mock)
        player_mock.get_inventory().has_sufficient_id_card.assert_called_with(npc_component.get_guard_type(),
                                                                              npc_component.get_guard_level())

        self.assertEqual(GUARD_ALLOWS, result)

    def test_guard_blocks_to_pass_on_incorrect_card(self):
        server_command_wrapper_mock = mock.Mock()

        client_command_dispatcher = ClientCommandDispatcher(server_command_wrapper_mock)

        player_mock = self.prepare_player_mock(False, (4, 10, 10))
        open_container_mem_mock = self.prepare_container_mem_mock(False)
        npc_component = self.prepare_npc_component("security", 3)
        server_level_mock = self.prepare_server_level_mock(
            is_walkable_result=WalkableResult(is_walkable=False,
                                              walking_blocked_type="guard",
                                              additional_information=npc_component),
            is_change_area_spot=False)

        player_service_client_mock = mock.Mock()
        player_service_client_mock.register_moving_player = mock.Mock()

        player_mock.get_inventory = mock.Mock()
        player_mock.get_inventory().has_sufficient_id_card = mock.Mock(return_value=False)

        result = client_command_dispatcher.handle_player_movement(server_level_mock,
                                                                  player_service_client_mock,
                                                                  player_mock,
                                                                  open_container_mem_mock,
                                                                  "0;1")

        self.assertEqual(0, player_mock.get_moving_component().start_moving.call_count)
        self.assertEqual(0, player_service_client_mock.register_moving_player.call_count)
        player_mock.get_inventory().has_sufficient_id_card.assert_called_with(npc_component.get_guard_type(),
                                                                              npc_component.get_guard_level())

        self.assertEqual(1, npc_component.parent.get_object_id.call_count)

        self.assertEqual(GUARD_DENYS, result)

    def test_default_walkable_result_works(self):
        server_command_wrapper_mock = mock.Mock()

        client_command_dispatcher = ClientCommandDispatcher(server_command_wrapper_mock)

        player_mock = self.prepare_player_mock(False, (1, 10, 10))
        open_container_mem_mock = self.prepare_container_mem_mock(False)
        server_level_mock = self.prepare_server_level_mock(WalkableResult(is_walkable=False,
                                                                          walking_blocked_type="default",
                                                                          additional_information=None),
                                                           False)

        result = client_command_dispatcher.handle_player_movement(server_level_mock,
                                                                  None,
                                                                  player_mock,
                                                                  open_container_mem_mock,
                                                                  "1;0")

        self.assertEqual(SRV_NO_MOVED, result)

    def test_area_change_hits(self):
        server_command_wrapper_mock = mock.Mock()

        client_command_dispatcher = ClientCommandDispatcher(server_command_wrapper_mock)

        player_mock = self.prepare_player_mock(False, (4, 10, 10))
        open_container_mem_mock = self.prepare_container_mem_mock(False)

        server_level_mock = self.prepare_server_level_mock(
            is_walkable_result=WalkableResult(is_walkable=False,
                                              walking_blocked_type="default",
                                              additional_information=None),
            is_change_area_spot=True)

        player_service_client_mock = mock.Mock()
        player_service_client_mock.register_moving_player = mock.Mock()

        player_mock.get_inventory = mock.Mock()
        player_mock.get_inventory().has_sufficient_id_card = mock.Mock(return_value=False)

        result = client_command_dispatcher.handle_player_movement(server_level_mock,
                                                                  player_service_client_mock,
                                                                  player_mock,
                                                                  open_container_mem_mock,
                                                                  "0;-1")

        player_mock.get_moving_component().start_moving.assert_called_with((4, 10, 9))
        player_service_client_mock.register_moving_player.assert_called_with(player_mock)

        self.assertEqual(AREA_CHANGE, result)

    def test_normal_walkable_field_works(self):
        server_command_wrapper_mock = mock.Mock()

        client_command_dispatcher = ClientCommandDispatcher(server_command_wrapper_mock)

        player_mock = self.prepare_player_mock(False, (4, 10, 10))
        open_container_mem_mock = self.prepare_container_mem_mock(False)

        server_level_mock = self.prepare_server_level_mock(
            is_walkable_result=WalkableResult(is_walkable=True,
                                              walking_blocked_type=None,
                                              additional_information=None),
            is_change_area_spot=False)

        player_service_client_mock = mock.Mock()
        player_service_client_mock.register_moving_player = mock.Mock()

        player_mock.get_inventory = mock.Mock()
        player_mock.get_inventory().has_sufficient_id_card = mock.Mock(return_value=False)

        result = client_command_dispatcher.handle_player_movement(server_level_mock,
                                                                  player_service_client_mock,
                                                                  player_mock,
                                                                  open_container_mem_mock,
                                                                  "-1;0")

        player_mock.get_moving_component().start_moving.assert_called_with((2, 9, 10))
        player_service_client_mock.register_moving_player.assert_called_with(player_mock)

        self.assertEqual(SRV_MOVED, result)

    def test_open_container_blocks_walking(self):
        server_command_wrapper_mock = mock.Mock()

        client_command_dispatcher = ClientCommandDispatcher(server_command_wrapper_mock)

        player_mock = self.prepare_player_mock(False, (4, 10, 10))
        open_container_mem_mock = self.prepare_container_mem_mock(True)

        result = client_command_dispatcher.handle_player_movement(None,
                                                                  None,
                                                                  player_mock,
                                                                  open_container_mem_mock,
                                                                  "-1;0")

        self.assertEqual(SRV_NO_MOVED_OPEN_CONTAINER, result)

    def test_already_moving_blocks_walking(self):
        server_command_wrapper_mock = mock.Mock()

        client_command_dispatcher = ClientCommandDispatcher(server_command_wrapper_mock)

        player_mock = self.prepare_player_mock(True, (4, 10, 10))

        result = client_command_dispatcher.handle_player_movement(None,
                                                                  None,
                                                                  player_mock,
                                                                  None,
                                                                  "-1;0")

        self.assertEqual(SRV_NO_MOVED_ALREADY_MOVING, result)