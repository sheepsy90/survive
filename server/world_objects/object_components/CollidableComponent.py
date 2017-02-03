# -*- coding:utf-8 -*-
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class CollidableComponent(AbstractComponent):

    def __init__(self):
        AbstractComponent.__init__(self, AbstractComponent.COLLIDABLE_COMPONENT)

        self.personal_value = "myvalue"

    def get_payload(self):
        return {
            "my_value": self.personal_value,
        }