# -*- coding:utf-8 -*-


class TutorialFlowHandler(object):

    def __init__(self, area_id):
        # TODO Make the tutorial Area ID Configurable
        self.tutorial_server = area_id == 3
        self.handles_player = False

    def is_tutorial_server(self):
        return self.tutorial_server

    def activate(self):
        self.handles_player = True

    def check(self):
        """ This method is called when there is no player connected -
            if we handled a player we need to reset the instance """
        return self.handles_player