# -*- coding:utf-8 -*-
from common.ItemTemplateTags import ItemTemplateTags
from server.scripting.intern.AbstractInternScript import AbstractInternScript
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class DoorHandlerAND(AbstractInternScript):
    """ This internal script is used for door opening and
        closing events. It checks each time its gets an event from the registered obhjects
        if it needs to update the effected world objects.

        It turns the visibility of those objects either on or off.

        It looks for the OPENED/CLOSED Tags and works in an AND fashion which
        means that only if all of the registered event suppliers have an OPENED Tag
        it will also hide the effected objects.
    """

    LABEL_KEY = "door_handler_and"

    def __init__(self, server_level, referenced_world_object, parameters):
        AbstractInternScript.__init__(self, server_level, referenced_world_object, parameters)

        self.world_object_manager = self.server_level.get_world_object_manager()

        self.list_of_doors = []

    def get_target_object_ids_from_parameter(self):
        list_of_objects = []
        try:
            single_door = int(self.parameters["objects"])
            list_of_objects.append(single_door)
        except Exception:
            list_of_objects = [int(e) for e in self.parameters["objects"].split(",")]
        return list_of_objects

    def initialize(self):
        target_objects = self.get_target_object_ids_from_parameter()

        self.list_of_doors = [self.world_object_manager.get_world_object_by_id(e) for e in target_objects]

    def handle_event(self, player, event_producing_world_object):
        """ This is the core Method of the script - it is called whenever a player tries to use that object """

        # First of all check if any of the event producers needs to change its internal state
        for element in self.registered_event_producer:
            element.get_component(AbstractComponent.USABLE_COMPONENT).check()

        can_open = True

        for element in self.registered_event_producer:
            print element.get_object_id(), element, element.tags
            if element.has_tag(ItemTemplateTags.CLOSED):
                can_open = False
                break

        if can_open:
            self.open_all_doors()
        else:
            self.close_all_doors()

    def open_all_doors(self):
        [e.set_visible(True) for e in self.list_of_doors]
        [self.server_level.push_world_object_changed_to_step_buffer_queue(e) for e in self.list_of_doors]

    def close_all_doors(self):
        [e.set_visible(False) for e in self.list_of_doors]
        [self.server_level.push_world_object_changed_to_step_buffer_queue(e) for e in self.list_of_doors]



