# -*- coding:utf-8 -*-
from numpy import array
import time


class MovableComponent():

    def __init__(self, position):
        self.discrete_position = position
        self.moving = False
        self.next_position = None
        self.started = None
        self.duration = 0.4
        self.interpolated_position = None

    def start_moving(self, target_position):
        self.next_position = target_position
        self.moving = True
        self.started = time.time()

    def is_moving(self):
        return self.moving

    def get_position_based_on_movement(self):
        if self.is_moving():
            position = self.get_interpolated_position()
        else:
            position = self.get_discrete_position()
        return position

    def is_moving_finished(self):
        current = time.time()
        if current >= self.started + self.duration:
            self.discrete_position = self.next_position
            self.moving = False
            self.started = None
            return True
        else:
            delta = ((self.started + self.duration) - current) / float(self.duration)
            self.interpolated_position = array(self.next_position)*(1-delta) + array(self.discrete_position)*delta
            self.interpolated_position[0] = self.next_position[0]
            self.interpolated_position = list(self.interpolated_position)
            return False

    def get_discrete_position(self):
        return self.discrete_position

    def get_interpolated_position(self):
        return self.interpolated_position

    @staticmethod
    def get_vector_by_direction(direction):
        if direction == 1: return [1, 0]
        if direction == 2: return [-1, 0]
        if direction == 3: return [0, 1]
        if direction == 4: return [0, -1]