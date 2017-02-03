# -*- coding:utf-8 -*-
import time


class MouseMemorizer():

    def __init__(self, gui_element):
        self.gui_element = gui_element
        self.gui_element.update = self.special_update_method

        self.old_mx = -1
        self.old_my = -1

        self.last_time_stable_mouse_position = -1

        self.mx = 0
        self.my = 0
        self.mb1 = 0
        self.mb2 = 0
        self.mb3 = 0

    def special_update_method(self, mx, my, mouse_buttons, events):
        self.gui_element.set_hover_state(mx, my)
        self.mx = mx
        self.my = my

        if mx != self.old_mx or my != self.old_my:
            self.last_time_stable_mouse_position = time.time()
            self.old_mx = mx
            self.old_my = my

        self.mb1 = mouse_buttons[0]
        self.mb2 = mouse_buttons[1]
        self.mb3 = mouse_buttons[2]

    def in_bounds(self, i, j, iend, jend):
        return i < self.mx < iend and j < self.my < jend

    def is_stable(self):
        return time.time() - self.last_time_stable_mouse_position > 0.25