# -*- coding:utf-8 -*-
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class UsableComponent(AbstractComponent):

    def __init__(self, initialized_script):
        AbstractComponent.__init__(self, AbstractComponent.USABLE_COMPONENT)
        self.initialized_script = initialized_script

    def get_script(self):
        return self.initialized_script

    def use(self, player, item):
        return self.initialized_script.use(player, item)

    def check(self):
        return self.initialized_script.check()