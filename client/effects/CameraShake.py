# -*- coding:utf-8 -*-

import math
import pygame
from pygame.rect import Rect
from client.colours import BLACK
from client.config import FPS, WINDOWHEIGHT, WINDOWWIDTH


class CameraShaker(object):

    def __init__(self):
        self.is_shaking = False
        self.shaking_stack = None

    def is_camera_shaking(self):
        return self.is_shaking

    def build_shaking_curve(self, amplitude, frequency, time_shaking):
        time_series = range(int(FPS*time_shaking))
        p_i_t = [e*(2*math.pi/FPS) for e in time_series]
        y_values = [int(amplitude*math.sin(e*frequency)) for e in p_i_t]
        value_reduction_factor = [(float(i)/len(y_values))**1.1 for i in range(len(y_values))]
        y_values = [int(y_values[i]*value_reduction_factor[i]) for i in range(len(y_values))]

        return p_i_t, y_values

    def perform(self, screen):
        if self.is_shaking:
            self.shake_step(screen)

    def shake_step(self, surface):
        if len(self.shaking_stack) > 0:
            element = self.shaking_stack.pop()
            surface.scroll(element)
            if element > 0:
                pygame.draw.rect(surface, BLACK, Rect(0, 0, element, WINDOWHEIGHT))
            elif element < 0:
                pygame.draw.rect(surface, BLACK, Rect(WINDOWWIDTH-element, 0, element, WINDOWHEIGHT))
        else:
            self.stop_shaking()

    def start_shaking(self, amplitude=15, frequency=10, time_shaking=2):
        self.is_shaking = True
        time_values, self.shaking_stack = self.build_shaking_curve(amplitude, frequency, time_shaking)

    def stop_shaking(self):
        self.is_shaking = False
        self.shaking_stack = None