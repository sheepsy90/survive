# -*- coding:utf-8 -*-
import time
from common.named_tuples import ScriptScheduleElement
from server.scripting.intern.AbstractInternScript import AbstractInternScript

from server.world_objects.object_components.AbstractComponent import AbstractComponent


class AlternateBetweenTwoLasers(AbstractInternScript):
    """
        This Internal Script takes two laser objects as input and alternates between them
        in a cycle with a defined duration.

        It depends on having exactly 2 arguments as target objects.
    """
    LABEL_KEY = "alternate_between_two_lasers"

    def __init__(self, server_level, referenced_world_object, parameters):
        AbstractInternScript.__init__(self, server_level, referenced_world_object, parameters)

        self.world_object_manager = self.server_level.get_world_object_manager()

        self.target_objects = []
        self.is_first_laser_active = True

        self.time_interval = 3
        self.last_execution = 0

    def get_target_object_ids_from_parameter(self):
        list_of_objects = []
        try:
            single_door = int(self.parameters["objects"])
            list_of_objects.append(single_door)
        except Exception:
            list_of_objects = [int(e) for e in self.parameters["objects"].split(",")]
        return list_of_objects

    def initialize(self):
        # Get the object ids
        list_of_object_ids = self.get_target_object_ids_from_parameter()

        assert len(list_of_object_ids) == 2, "This Script only supports two alternating Lasers"

        self.target_objects = [self.world_object_manager.get_world_object_by_id(e) for e in list_of_object_ids]

        # Make sure they all have a laser component
        for world_object in self.target_objects:
            assert world_object.has_component(AbstractComponent.LASER_COMPONENT)

        self.schedule_this()

    def is_time(self):
        if (time.time() - self.last_execution) > self.time_interval:
            self.last_execution = time.time()
            return True
        return False

    def handle_event(self, player, event_producing_world_object):
        """ This is the core Method of the script - it is called whenever a player tries to use that object """

        self.schedule_this()

        if self.is_time():
            self.switch_state()

    def switch_state(self):
        if self.is_first_laser_active:
            self.is_first_laser_active = False
            self.target_objects[0].get_component(AbstractComponent.LASER_COMPONENT).set_active(True)
            self.target_objects[1].get_component(AbstractComponent.LASER_COMPONENT).set_active(False)
        else:
            self.is_first_laser_active = True
            self.target_objects[1].get_component(AbstractComponent.LASER_COMPONENT).set_active(True)
            self.target_objects[0].get_component(AbstractComponent.LASER_COMPONENT).set_active(False)

        [self.server_level.push_world_object_changed_to_step_buffer_queue(e) for e in self.target_objects]

    def schedule_this(self):
        self.server_level.get_intern_script_manager().schedule_script_call(
            ScriptScheduleElement(self.script_id, time.time() + 0.1))