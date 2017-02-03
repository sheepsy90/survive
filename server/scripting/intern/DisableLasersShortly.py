# -*- coding:utf-8 -*-
import time
from common.named_tuples import ScriptScheduleElement
from server.scripting.intern.AbstractInternScript import AbstractInternScript
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class DisableLasersShortly(AbstractInternScript):

    LABEL_KEY = "disable_lasers_shortly"

    """
        This script is used to disable a set of lasers for a short period of time when one of the
        registered event providers has the tag OPENED in them. The script schedules itself again in the
         internal script cycle if its state results in a turned of laser such that it is reevaluated again
         after a short period of time.
    """

    def __init__(self, server_level, referenced_world_object, parameters):
        AbstractInternScript.__init__(self, server_level, referenced_world_object, parameters)

        self.world_object_manager = self.server_level.get_world_object_manager()
        self.target_objects = []

        self.laser_deactivated_last_time = 0
        self.laser_off_time = 1

    def get_target_object_ids_from_parameter(self):
        list_of_objects = []
        try:
            single_door = int(self.parameters["objects"])
            list_of_objects.append(single_door)
        except Exception:
            list_of_objects = [int(e) for e in self.parameters["objects"].split(",")]
        return list_of_objects

    def initialize(self):
        # First we get the target object ids
        list_of_object_ids = self.get_target_object_ids_from_parameter()

        # Get the actual world objects
        self.target_objects = [self.world_object_manager.get_world_object_by_id(e) for e in list_of_object_ids]

        # Make sure they all have a laser component
        for world_object in self.target_objects:
            assert world_object.has_component(AbstractComponent.LASER_COMPONENT)

    def handle_event(self, player, event_producing_world_object):
        """ This is the core Method of the script - it is called whenever a player tries to use that object """

        if player is None and event_producing_world_object is None:
            # Its a call from the internal system so we need to check if the time the laser is kept
            # off over and turn it on again
            if (time.time() - self.laser_deactivated_last_time) > self.laser_off_time:
                [world_object.get_component(AbstractComponent.LASER_COMPONENT).set_active(True)
                 for world_object in self.target_objects]

                [self.server_level.push_world_object_changed_to_step_buffer_queue(e)
                 for e in self.target_objects]
            else:
                self.schedule_this()
        else:
            # A player interacted with this script and therefore we need to check if the laser needs to be
            # turned of

            self.laser_deactivated_last_time = time.time()

            [world_object.get_component(AbstractComponent.LASER_COMPONENT).set_active(False)
             for world_object in self.target_objects]

            [self.server_level.push_world_object_changed_to_step_buffer_queue(e)
             for e in self.target_objects]

            self.schedule_this()

    def schedule_this(self):
        self.server_level.get_intern_script_manager().schedule_script_call(
            ScriptScheduleElement(self.script_id, time.time() + 0.1))