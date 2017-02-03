# -*- coding:utf-8 -*-

class AbstractComponent():

    SCRIPT_COMPONENT = "SCRIPT_COMPONENT"
    NPC_COMPONENT = "NPC_COMPONENT"
    COLLIDABLE_COMPONENT = "COLLIDABLE_COMPONENT"
    STEPABLE_COMPONENT = "STEPABLE_COMPONENT"
    CONTAINER_COMPONENT = "CONTAINER_COMPONENT"
    USABLE_COMPONENT = "USABLE_COMPONENT"
    LASER_COMPONENT = "LASER_COMPONENT"
    MINE_COMPONENT = "MINE_COMPONENT"

    def __init__(self, name):
        self.name = name
        self.parent = None

    def get_property_name(self):
        return self.name

    def set_parent(self, parent):
        self.parent = parent

    def get_parent_object_id(self):
        return self.parent.get_object_id()

    def get_payload(self):
        """ This is the specific payload method that needs to be overwritten by each component.
            What is specified as a dictionary return within this method is parsed into JSON and
            send to the client with the Component Key - Don't overwriting it results in no entry
            in the dictionary that is send"""
        return None