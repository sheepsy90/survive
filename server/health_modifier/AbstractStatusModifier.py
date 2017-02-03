# -*- coding:utf-8 -*-


class AbstractStatusModifier():

    def __init__(self, name, type, visible=True):
        self.name = name
        self.type = type
        self.visible = visible

    def is_visible(self):
        return self.visible

    def ongoing_effect(self, player, status_modifier_component):
        pass

    def queue_time_is_up(self, player, status_modifier_component):
        pass

    def added_to_queue(self, player, status_modifier_component):
        return True

    def get_type(self):
        return self.type

