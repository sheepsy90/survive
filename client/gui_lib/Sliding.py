# -*- coding:utf-8 -*-
import time

class SlidingEffectChain(object):

    def __init__(self):
        self.chain = []

    def add_sliding_effect(self, effect):
        self.chain.append(effect)

    def execute(self):
        if len(self.chain) > 0:
            if self.chain[0].execute():
                del self.chain[0]
            return False
        return True


class SlidingEffectParallel(object):

    def __init__(self):
        self.sliding_set = []

    def add_sliding_effect(self, effect):
        self.sliding_set.append(effect)

    def execute(self):
        for element in self.sliding_set:
            if element.execute():
                return True
        return False

class SlidingEffect(object):

    def __init__(self, gui_element, x=None, y=None, duration=1.0):
        self.gui_element = gui_element
        self.end_x = x
        self.end_y = y
        self.duration = duration
        self.started = False

    def execute(self):
        if not self.started:
            self.start_x = self.gui_element.x
            self.start_y = self.gui_element.y
            self.start_t = time.time()
            self.end_t = self.start_t + self.duration
            self.started = True

        delta = (time.time() - self.start_t) / float(self.duration)

        if delta > 1.0:
            if self.end_y is not None:
                self.gui_element.y = self.end_y
            if self.end_x is not None:
                self.gui_element.x = self.end_x
            return True

        if self.end_y is not None:
            self.gui_element.y = self.start_y*(1-delta) + self.end_y*(delta)
        if self.end_x is not None:
            self.gui_element.x = self.start_x*(1-delta) + self.end_x*(delta)

        return False


class OpeningEffect(object):

    def __init__(self, gui_element, x_start, y_start, width, height, open=True, duration=1.0):
        self.gui_element = gui_element
        self.start_x = x_start
        self.start_y = y_start
        self.open=open
        self.width = width
        self.height = height
        self.duration = duration
        self.started = False

    def execute(self):
        if not self.started:
            self.start_t = time.time()
            self.end_t = self.start_t + self.duration
            self.started = True

        delta = (time.time() - self.start_t) / float(self.duration)

        if delta > 1.0:
            self.gui_element.x = self.start_x - self.width/2
            self.gui_element.y = self.start_y - self.height/2
            self.gui_element.width = self.width
            self.gui_element.height = self.height
            return True

        self.gui_element.x = self.start_x - int(delta*self.width/2)
        self.gui_element.y = self.start_y - int(delta*self.height/2)
        self.gui_element.width = int(self.width*delta)
        self.gui_element.height = int(self.height*delta)

        return False
