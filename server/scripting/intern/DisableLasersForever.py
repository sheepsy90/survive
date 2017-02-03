# -*- coding:utf-8 -*-
from common.ItemTemplateTags import ItemTemplateTags
from server.scripting.intern.AbstractInternScript import AbstractInternScript
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class DisableLasersForever(AbstractInternScript):

    LABEL_KEY = "disable_lasers_forever"

    """
        This script is used to disable a set of lasers forever when one of the
        registered event providers has the tag OPENED in them - it is not possible
        that this script alters the state again afterwards.
    """

    def __init__(self, server_level, referenced_world_object, parameters):
        AbstractInternScript.__init__(self, server_level, referenced_world_object, parameters)

        self.world_object_manager = self.server_level.get_world_object_manager()
        self.target_objects = []

        self.laser_deactivated = False

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

        if self.laser_deactivated:
            return

        # First of all check if any of the event producers needs to change its internal state
        for element in self.registered_event_producer:
            element.get_component(AbstractComponent.USABLE_COMPONENT).check()

        for element in self.registered_event_producer:
            if element.has_tag(ItemTemplateTags.OPENED):
                self.laser_deactivated = True
                break

        [world_object.get_component(AbstractComponent.LASER_COMPONENT).set_active(False)
         for world_object in self.target_objects]

        [self.server_level.push_world_object_changed_to_step_buffer_queue(e)
         for e in self.target_objects]


