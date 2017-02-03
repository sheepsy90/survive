# -*- coding:utf-8 -*-
import unittest
from common.ItemTemplateTags import ItemTemplateTagConsistencyChecker

from common.LevelLoader import LevelFactory
from client.local_objects.FullClientLevel import FullClientLevel


def load_level_for_client(id, prefix=""):
    ItemTemplateTagConsistencyChecker.check()
    level_factory = LevelFactory()
    level_template = level_factory.load_level_by_id(id, prefix=prefix)
    layers = level_template.get_level_layers()
    tile_coordinate_mapping = level_template.get_coordinate_mapping()
    full_server_level = FullClientLevel(level_template.get_identifier(),
                                        level_template.get_size(),
                                        layers,
                                        tile_coordinate_mapping,
                                        level_template.build_walk_map())
    return full_server_level


class TestLevelManager(unittest.TestCase):

    def test_tutorial_load_for_server(self):
        print load_level_for_client(3, prefix="../../")

    def test_level_after_tutorial_load_for_server(self):
        print load_level_for_client(1, prefix="../../")

    def test_level_left_loads(self):
        print load_level_for_client(4, prefix="../../")

    def test_level_right_loads(self):
        print load_level_for_client(5, prefix="../../")

    def test_level_common_room_loads(self):
        print load_level_for_client(6, prefix="../../")

    def test_level_first_puzzle_loads(self):
        print load_level_for_client(7, prefix="../../")
