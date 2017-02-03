# -*- coding:utf-8 -*-


class AbstractRobotScript():

    def __init__(self, enemy_system_buffer_queue, pathway_list, list_of_robots):
        self.pathway_list = pathway_list
        self.list_of_robots = list_of_robots
        self.enemy_system_buffer_queue = enemy_system_buffer_queue

    def initialize(self):
        """ This method is called immediately after the creation and makes
            sure the robots are placed correctly initially """
        pass

    def perform(self):
        raise NotImplementedError("The robot script needs some behaviour")