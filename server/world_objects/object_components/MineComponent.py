# -*- coding:utf-8 -*-
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class MineComponent(AbstractComponent):
    """ This Component can be attached to a world object to make it a mine.
        Currently there is not much logic available but the sending to the client.
    """

    def __init__(self, radius):
        AbstractComponent.__init__(self, AbstractComponent.MINE_COMPONENT)

        self.radius = radius

    def get_payload(self):
        return {
            "radius": self.radius,
        }