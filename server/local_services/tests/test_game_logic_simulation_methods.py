# -*- coding:utf-8 -*-
"""

^^^^^^^^^^^^

.. moduleauthor:: sheepy <sheepy@informatik.uni-hamburg.de>

History:
* 07.02.15: Created (sheepy)

"""
import unittest
import mock
from server.health_modifier.HungerThirstModifier import HungerIncreaseModifier
from server.health_modifier.SpecifiedModifiers import PoisonedModifier
from server.local_services.GameLogicSimulationMethods import GameLogicSimulationMethods


class TestGameLogicSimulationMethods(unittest.TestCase):

    def prepare_player_modifier_mock(self, health_modifier):
        get_health_modifier_component = mock.Mock()
        get_health_modifier_component.get_modifiers = mock.Mock(return_value=health_modifier)

        player_mock = mock.Mock()
        player_mock.get_health_modifier_component = mock.Mock(return_value=get_health_modifier_component)

        self.assertEqual(player_mock.get_health_modifier_component().get_modifiers(), health_modifier)
        return player_mock

    def test_character_condition_properties(self):
        glsm = GameLogicSimulationMethods(None, None, None, None, None)

        player_mock = self.prepare_player_modifier_mock({PoisonedModifier.TYPE_ID: 1,
                                                         HungerIncreaseModifier.TYPE_ID: 5})

        char_condition_property = glsm.calculate_character_condition_properties(player_mock)

        self.assertEqual(True, char_condition_property.alive)
        self.assertEqual(12, char_condition_property.redness)
        self.assertEqual(2, char_condition_property.blurriness)

    def test_character_condition_properties_second(self):
        glsm = GameLogicSimulationMethods(None, None, None, None, None)

        player_mock = self.prepare_player_modifier_mock({PoisonedModifier.TYPE_ID: 1,
                                                         HungerIncreaseModifier.TYPE_ID: 4})

        char_condition_property = glsm.calculate_character_condition_properties(player_mock)

        self.assertEqual(True, char_condition_property.alive)
        self.assertEqual(10, char_condition_property.redness)
        self.assertEqual(1, char_condition_property.blurriness)

