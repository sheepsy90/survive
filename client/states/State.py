# -*- coding:utf-8 -*-
class State(object):

    def enter_state(self, properties):
        pass

    def exit_state(self):
        pass

    def update(self):
        raise NotImplementedError("Update Cycle not implemented!")