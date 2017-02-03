# -*- coding:utf-8 -*-
import time
from server.local_services.Bullet import Bullet


class BulletSystem(object):

    def __init__(self):
        self.current_id = 0
        self.bullets = []

    def add_bullet(self, direction, start_posx, start_posy):
        id = self.current_id + 1
        self.current_id += 1
        start_time = time.time()
        self.bullets.append(Bullet(id, direction, start_posx, start_posy, start_time))

    def calculate_all_bullet_positions(self):
        for bullet in self.bullets:
            bullet.calculate_current_position()

    def get_bullets_marked_destroyed(self):
        return [b for b in self.bullets if b.is_marked_hit()]

    def remove_destroyed_bullets(self):
        self.bullets = [b for b in self.bullets if not b.is_marked_hit()]

    def get_bullets(self):
        return self.bullets