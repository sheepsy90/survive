# -*- coding:utf-8 -*-
import time


class AbstractUsableScript():

    def __init__(self, server_level, referenced_world_object, parameters):
        self.server_level = server_level
        self.referenced_world_object = referenced_world_object
        self.parameters = parameters
        self.usage_cool_down = 0
        self.last_time_used = 0

    def initialize(self):
        raise NotImplementedError("This method is used to extract values from the parameters")

    def use(self, player, item):
        """ This is the core Method of the script - it is called whenever a player tries to use that object """
        raise NotImplementedError("This is the Abstract definition of a Usable Script")

    def check(self):
        """ This method checks for internal state changes and returns True if the state has changed """
        return False

    def uses_bare_hands(self, item):
        return item is None

    def check_cool_down_over(self):
        if time.time() - self.last_time_used > self.usage_cool_down:
            self.last_time_used = time.time()
            return True
        return False

