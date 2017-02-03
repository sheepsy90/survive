# -*- coding:utf-8 -*-
from server.health_modifier.AbstractStatusModifier import AbstractStatusModifier


class ThirstIncreaseModifier(AbstractStatusModifier):

    TYPE_ID = 5

    def __init__(self):
        AbstractStatusModifier.__init__(self, "Thirst", ThirstIncreaseModifier.TYPE_ID)

    def queue_time_is_up(self, player, health_system):

        if health_system.get_status_type_count(ThirstCompensationModifier.TYPE_ID) > 0:
            health_system.decrease_modifier(ThirstCompensationModifier.TYPE_ID, 1)
        else:
            if health_system.get_status_type_count(self.get_type()) < 10:
                health_system.increase_modifier(self.get_type(), 1)


class HungerIncreaseModifier(AbstractStatusModifier):

    TYPE_ID = 6

    def __init__(self):
        AbstractStatusModifier.__init__(self, "HungerIncrease", HungerIncreaseModifier.TYPE_ID)

    def queue_time_is_up(self, player, status_modifier_component):
        if status_modifier_component.get_status_type_count(HungerCompensationModifier.TYPE_ID) > 0:
            status_modifier_component.decrease_modifier(HungerCompensationModifier.TYPE_ID, 1)
        else:
            if status_modifier_component.get_status_type_count(self.get_type()) < 10:
                status_modifier_component.increase_modifier(self.get_type(), 1)


class ThirstCompensationModifier(AbstractStatusModifier):

    TYPE_ID = 7

    def __init__(self):
        AbstractStatusModifier.__init__(self, "ThirstCompensation", ThirstCompensationModifier.TYPE_ID)

    def queue_time_is_up(self, player, status_modifier_component):
        if status_modifier_component.get_status_type_count(ThirstIncreaseModifier.TYPE_ID) > 0:
            status_modifier_component.decrease_modifier(ThirstIncreaseModifier.TYPE_ID, 1)
        else:
            if status_modifier_component.get_status_type_count(self.get_type()) < 10:
                status_modifier_component.increase_modifier(self.get_type(), 1)


class HungerCompensationModifier(AbstractStatusModifier):

    TYPE_ID = 8

    def __init__(self):
        AbstractStatusModifier.__init__(self, "HungerCompensation", HungerCompensationModifier.TYPE_ID)

    def queue_time_is_up(self, player, status_modifier_component):
        if status_modifier_component.get_status_type_count(HungerIncreaseModifier.TYPE_ID) > 0:
            status_modifier_component.decrease_modifier(HungerIncreaseModifier.TYPE_ID, 1)
        else:
            if status_modifier_component.get_status_type_count(self.get_type()) < 10:
                status_modifier_component.increase_modifier(self.get_type(), 1)
