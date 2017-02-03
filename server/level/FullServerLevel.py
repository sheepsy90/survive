# -*- coding:utf-8 -*-
import logging

from common.named_tuples import WalkableResult
from server.local_services.SimulationStepObjectBufferQueueSystem import SimulationStepBufferQueue
from server.local_services.EnemySystem import EnemySystem
from server.scripting.InternScriptManager import InternScriptManager
from server.world_objects.WorldObjectManager import WorldObjectManager
from server.world_objects.object_components.AbstractComponent import AbstractComponent

from server.constants.string_constants import GUARD_WALKABLE_TYPE

logger = logging.getLogger(__name__)

#TODO Make the position checks for the walking faster by defining a bit mask or something like that


class FullServerLevel(object):
    """ This class represents a level on the server side with all it's needs
        This for example excludes all things about the graphic layers """

    def __init__(self, level_id, level_size, tiled_objects, tiled_scripts, tiled_enemies, walk_map, robot_movement_map, atmospheric_data, area_transitions):
        # Parameters we get in from outside
        self.level_id = level_id
        self.level_size = level_size
        self.width, self.height = level_size
        self.walk_map = walk_map
        self.robot_movement_map = robot_movement_map
        self.atmospheric_data = atmospheric_data
        self.tiled_enemies = tiled_enemies

        # Some internal parameters
        self.area_change_spots = {}
        [self.add_area_change_spot(e) for e in area_transitions]

        self.world_object_manager = WorldObjectManager(level_id)
        self.world_object_manager.build_objects(self, tiled_objects)

        self.intern_script_manager = InternScriptManager(level_id)
        self.intern_script_manager.build_internal_scripts(self, tiled_scripts)
        self.intern_script_manager.initialize_scripts()

        self.world_object_manager.initialize_usable_scripts()

    def prepare(self, sim_step_buffer_queue_sys):
        """ This method is called to prepare the Server Level by injecting the necessary handlers and systems """
        self.sim_step_buffer_queue_system = sim_step_buffer_queue_sys

        # Create a locale Enemy Service and spawn enemies
        self.local_enemy_system = EnemySystem(self, self.tiled_enemies, self.sim_step_buffer_queue_system)
        self.local_enemy_system.initialize_enemies()

    def push_world_object_changed_to_step_buffer_queue(self, world_object):
        self.sim_step_buffer_queue_system.push(SimulationStepBufferQueue.WORLD_OBJECTS_CHANGED, world_object)

    def get_enemy_system(self):
        return self.local_enemy_system

    def get_atmospheric_data(self):
        return self.atmospheric_data

    def get_level_dimensions(self):
        return self.level_size

    def get_world_object_manager(self):
        return self.world_object_manager

    def get_intern_script_manager(self):
        return self.intern_script_manager

    def can_search_spot(self, px, py):
        """ This method returns with a GameObject related to the position requested when it is able to search
            else None """
        for world_object in self.world_object_manager.get_values_from_component_cache(AbstractComponent.CONTAINER_COMPONENT):
            if world_object.is_visible():
                mfx, mfy = world_object.get_middle_foot_point()
                print mfx, mfy, px, py
                if px == mfx and py == mfy:
                    return world_object
        return None

    def get_usable_component_for_spot(self, px, py):
        for world_object in self.world_object_manager.get_values_from_component_cache(AbstractComponent.USABLE_COMPONENT):
            pi, pj = world_object.get_middle_foot_point()
            if pi == px and pj == py:
                return world_object
        return None

    def get_npc_component_for_spot(self, px, py):
        for world_object in self.world_object_manager.get_values_from_component_cache(AbstractComponent.NPC_COMPONENT):
            pi, pj = world_object.get_middle_foot_point()
            if pi == px and pj == py:
                return world_object
        return None

    def add_area_change_spot(self, area_change_spot):
        """ This methods defines spots on the map as area change spots which result in an area change when the player
            steps on such a spot """
        i, j = area_change_spot.get_source_coordinates()
        if not self.area_change_spots.__contains__(i):
            self.area_change_spots[i] = {}

        # Add the area change spot object to the dictionary
        self.area_change_spots[i][j] = area_change_spot

    def is_change_area_spot(self, i, j):
        """ This method requests if the spot on the map is an area change spot or not.
            If that spot is an area change spot it returns the information associated with that
            change spot, otherwise it returns None """
        if i not in self.area_change_spots:
            return False

        if j not in self.area_change_spots[i]:
            return False

        return True

    def get_change_area(self, i, j):
        return self.area_change_spots[i][j]

    def is_walkable(self, i, j):
        """ This method shall determine if a spot is walkable on the level.
            This for now only includes a check on the predefined accessability layer """
        if not (0 <= i < self.width and 0 <= j < self.height):
            return WalkableResult(is_walkable=False, walking_blocked_type='bounds', additional_information=None)

        walk_map_result = self.walk_map[i][j] == 0

        if not walk_map_result:
            return WalkableResult(is_walkable=False, walking_blocked_type='default', additional_information=None)

        for element in self.world_object_manager.get_values_from_component_cache(AbstractComponent.COLLIDABLE_COMPONENT):
            if element.is_visible():
                pi, pj = element.get_middle_foot_point()
                if i == pi and j == pj:
                    return WalkableResult(is_walkable=False, walking_blocked_type='collidable',
                                          additional_information=None)

        for world_object in self.world_object_manager.get_values_from_component_cache(AbstractComponent.NPC_COMPONENT):
            npc_component = world_object.get_component(AbstractComponent.NPC_COMPONENT)
            if npc_component.is_guard():
                mx, my = world_object.get_middle_foot_point()
                if npc_component.does_guard_apply(i, j, mx, my):
                    logger.warning("Player can't pass through that spot because the guard is there.")
                    return WalkableResult(is_walkable=False,
                                          walking_blocked_type=GUARD_WALKABLE_TYPE,
                                          additional_information=npc_component)

        return WalkableResult(is_walkable=True, walking_blocked_type=None, additional_information=None)

    def is_robot_walkable(self, i, j):
        """ This method shall determine if a spot is walkable on the level.
            This for now only includes a check on the predefined accessability layer """
        if not (0 <= i < self.width and 0 <= j < self.height):
            return False

        return self.robot_movement_map[i][j] == 1

    def get_level_identifier(self):
        return self.level_id
