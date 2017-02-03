# -*- coding:utf-8 -*-
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class NpcComponent(AbstractComponent):

    GUARD_TYPE_SECURITY = "security"
    GUARD_TYPE_ADMINISTRATION = "administration"
    GUARD_TYPE_SCIENCE = "science"
    GUARD_TYPE_TECHNICIAN = "technician"

    def __init__(self, npc_properties):
        AbstractComponent.__init__(self, AbstractComponent.NPC_COMPONENT)
        self.npc_properties = npc_properties

        self.guard_level = None
        if self.npc_properties.npc_guard_level is not None:
            self.guard_level = int(self.npc_properties.npc_guard_level)

    def get_npc_type(self):
        return self.npc_properties.npc_type

    def is_guard(self):
        return self.npc_properties.is_guard

    def does_guard_apply(self, i, j, mx, my):
        if self.npc_properties.npc_guard_orientation == "left":
            mx -= 1
        elif self.npc_properties.npc_guard_orientation == "right":
            mx += 1

        if i == mx and j == my:
            return True

    def get_guard_type(self):
        return self.npc_properties.npc_guard_type

    def get_guard_level(self):
        return self.guard_level