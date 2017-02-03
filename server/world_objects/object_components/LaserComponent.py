# -*- coding:utf-8 -*-
from common.constants.Directions import Directions
from server.world_objects.object_components.AbstractComponent import AbstractComponent


class LaserComponent(AbstractComponent):
    """ This Component is attached to a laser object meaning a world object which puts out a laser
        which then runs several fields wide. If the player runs into the laser he will be damaged.
        We need to figure out how the visible/active state is transmitted.
    """

    def __init__(self, distance, direction=Directions.DOWN):
        AbstractComponent.__init__(self, AbstractComponent.LASER_COMPONENT)

        self.distance = distance
        self.direction = direction
        self.active = True

    def get_payload(self):
        return {
            "distance": self.distance,
            "direction": self.direction,
            "active": self.active
        }

    def set_active(self, value):
        self.active = value