# -*- coding:utf-8 -*-
from server.health_modifier.AbstractStatusModifier import AbstractStatusModifier


class SimpleDamageModifier(AbstractStatusModifier):

    TYPE_ID = 301

    def __init__(self):
        AbstractStatusModifier.__init__(self, "SimpleDamageModifier", SimpleDamageModifier.TYPE_ID)

    def queue_time_is_up(self, player, status_modifier_component):
        if status_modifier_component.get_status_type_count(self.get_type()) < 10:
            status_modifier_component.increase_modifier(self.get_type(), 1)


class ShockedDamageModifier(AbstractStatusModifier):

    TYPE_ID = 302

    def __init__(self):
        AbstractStatusModifier.__init__(self, "ShockedDamageModifier", ShockedDamageModifier.TYPE_ID)

    def queue_time_is_up(self, player, status_modifier_component):
        if status_modifier_component.get_status_type_count(self.get_type()) < 10:
            status_modifier_component.increase_modifier(self.get_type(), 1)
