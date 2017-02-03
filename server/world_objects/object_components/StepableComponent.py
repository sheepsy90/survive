# -*- coding:utf-8 -*-
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class StepableComponent(AbstractComponent):

    def __init__(self, active=False):
        AbstractComponent.__init__(self, AbstractComponent.STEPABLE_COMPONENT)
        self.active = active

    def is_active(self):
        return self.active

    def update(self, new_state):
        if new_state != self.active:
            print "UPDATE STEP COMPOnENT"
            self.active = new_state
            return True
        return False

    def get_reference_position(self):
        return self.parent.get_middle_foot_point()