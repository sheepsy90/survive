# -*- coding:utf-8 -*-
import time
from server.components.MovableComponent import MovableComponent


class Bullet():

    def __init__(self, id, direction, start_posx, start_posy, start_time):
        self.id = id
        self.direction = direction
        self.start_posx = start_posx
        self.start_posy = start_posy
        self.start_time = start_time
        self.speed = 16
        self.lifetime = 4

        self.current_x = start_posx
        self.current_y = start_posy
        self.marked_hit = False

    def calculate_current_position(self):
        current_time = time.time()
        if current_time > self.start_time + self.lifetime:
            self.mark_hit()

        xd, yd = MovableComponent.get_vector_by_direction(self.direction)

        # TODO aufgrund der 4 richtungen ist jeweils nur eine zeile wirklich zu berechnen
        self.current_x = self.start_posx + (current_time - self.start_time)*self.speed*xd
        self.current_y = self.start_posy + (current_time - self.start_time)*self.speed*yd

    def get_bullet_x(self):
        return self.current_x

    def get_bullet_y(self):
        return self.current_y

    def get_bullet_id(self):
        return self.id

    def mark_hit(self):
        self.marked_hit = True

    def is_marked_hit(self):
        return self.marked_hit

    def get_damage(self):
        return 1