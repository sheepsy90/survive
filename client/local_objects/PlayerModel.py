# -*- coding:utf-8 -*-
from numpy import array
import time


class PlayerModel(object):

    def __init__(self, player_id, player_name, position, is_moving):
        self.player_id = player_id
        self.player_name = player_name
        self.position = array(position)
        self.moving = is_moving
        self.moving_timer = None
        self.bluriness = 1
        self.redness = 0

    def update_moving(self, moving_bool):
        if not self.moving and moving_bool:
            # We start with moving so we set a start timer
            self.moving_timer = time.time()
        elif self.moving and not moving_bool:
            # We reset that timer
            self.moving_timer = None

        # Set the actual value
        self.moving = moving_bool

    def get_moving_timer(self):
        return self.moving_timer

    def update_position(self, position, moving):
        self.update_moving(moving)
        self.position = position

    def get_position(self):
        return self.position

    def get_name(self):
        return self.player_name

    def get_player_id(self):
        return self.player_id

    def is_moving(self):
        return self.moving

    def get_health_properties(self):
        return self.bluriness, self.redness

    def set_character_condition(self, bluriness, redness):
        self.bluriness = bluriness
        self.redness = redness