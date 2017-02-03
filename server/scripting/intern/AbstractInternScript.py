# -*- coding:utf-8 -*-


class AbstractInternScript():

    def __init__(self, script_id, parameters, server_level):
        self.script_id = script_id
        self.server_level = server_level
        self.parameters = parameters

        self.registered_event_producer = []

    def get_script_id(self):
        return self.script_id

    def initialize(self):
        raise NotImplementedError("This method is used to extract values from the parameters")

    def register(self, world_object):
        print "REgistered Usable SCript at Intern Script", world_object
        """ This method is necessary such that all event provider can register themselves here to get checked again """
        self.registered_event_producer.append(world_object)

    def handle_event(self, player, event_producing_world_object):
        """ This is the core Method of the script - it is called whenever a player tries to use that object """
        raise NotImplementedError("This is the Abstract definition of a Usable Script")