import os

from common.AreaChangeSpot import AreaChangeSpot
from common.constants.ServerToClientNetworkCommands import LOOK_LEFT, LOOK_RIGHT
from server.level.server_level_loader import load_level_for_server
from server.xmlrpc_services.crafting.CraftingServiceClient import CraftingServiceClient
from server.xmlrpc_services.items.ItemServiceClient import ItemServiceClient


class SteppingRule(object):

    def __init__(self, stepables_down_required, world_objects_not_visible):
        self.stepables_down_required = stepables_down_required
        self.world_objects_not_visible = world_objects_not_visible
        self.state = False

    def get_required_stepable_object_ids(self):
        return self.stepables_down_required

    def get_visibility_effected_object_ids(self):
        return self.world_objects_not_visible

    def change_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            return True
        return False


class AreaService():

    def __init__(self):
        self.area_dict = {
            1: self.create_after_tutorial_level,
            3: self.create_tutorial_level,
            4: self.create_left_01_level,
            5: self.create_right_02_level,
            6: self.create_common_room,
            7: self.create_first_puzzle_level,
            8: self.create_two_player_puzzle
        }

        self.crafting_service_client = CraftingServiceClient()
        self.item_service_client = ItemServiceClient()

    def get_area_specifications(self, area_code):
        assert area_code in self.area_dict
        creator = self.area_dict[area_code]
        if creator is not None:
            return creator()
        return None

    @staticmethod
    def create_after_tutorial_level():
        server_level = load_level_for_server(os.path.abspath("resources/levels/after_tutorial_level.json"))

        server_level.add_area_change_spot(AreaChangeSpot(source_position=(0, 20),
                                                         target_level_id=4,
                                                         target_position=(LOOK_LEFT, 79, 113)))

        server_level.add_area_change_spot(AreaChangeSpot(source_position=(59, 20),
                                                         target_level_id=5,
                                                         target_position=(LOOK_RIGHT, 0, 33)))

        return server_level


    @staticmethod
    def create_left_01_level():
        server_level = load_level_for_server(os.path.abspath("resources/levels/level_01_left.json"))

        server_level.add_area_change_spot(AreaChangeSpot(source_position=(79, 113),
                                                         target_level_id=1,
                                                         target_position=(LOOK_RIGHT, 0, 20)))

        return server_level

    @staticmethod
    def create_right_02_level():
        server_level = load_level_for_server(os.path.abspath("resources/levels/level_02_right.json"))

        server_level.add_area_change_spot(AreaChangeSpot(source_position=(0, 33),
                                                         target_level_id=1,
                                                         target_position=(LOOK_LEFT, 59, 20)))
        return server_level

    @staticmethod
    def create_tutorial_level():
        server_level = load_level_for_server(os.path.abspath("resources/levels/level_tutorial.json"))

        return server_level

    @staticmethod
    def create_common_room():
        server_level = load_level_for_server(os.path.abspath("resources/levels/common_room.json"))
        return server_level

    @staticmethod
    def create_first_puzzle_level():
        server_level = load_level_for_server(os.path.abspath("resources/levels/first_puzzle_test.json"))
        return server_level

    @staticmethod
    def create_two_player_puzzle():

        server_level = load_level_for_server(os.path.abspath("resources/levels/two_player_puzzle.json"))
        return server_level
