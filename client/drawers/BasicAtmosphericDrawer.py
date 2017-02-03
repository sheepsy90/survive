# -*- coding:utf-8 -*-
import random
from client.config import CELLSIZE, PLAYER_CENTER_X, PLAYER_CENTER_Y


class BasicAtmosphericDrawer():

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager

        NUM_ANIMS = 50
        TIME_EACH = 2

        self.pool = [
            self.resource_manager.load_animation("athmospherics", 10, [TIME_EACH for i in range(10)], loop=True) for i in range(NUM_ANIMS)
        ]

        [e.play(random.random()*TIME_EACH*10) for e in self.pool]

        self.random_mapping = {}

    def get_anim_for_c(self, ii, jj):
        if ii not in self.random_mapping:
            self.random_mapping[ii] = {}
        if jj not in self.random_mapping[ii]:
            self.random_mapping[ii][jj] = random.choice(self.pool)
        return self.random_mapping[ii][jj]

    def calculate_layer_data_indices(self, px, py, i, j):
        ii = int(px) - PLAYER_CENTER_X + i
        jj = int(py) - PLAYER_CENTER_Y + j

        return ii, jj

    def draw_s(self, i, j, ox, oy, offset, renderer, ii, jj):


        x = (i + offset) * CELLSIZE - int(ox * CELLSIZE)
        y = (j + offset) * CELLSIZE - int(oy * CELLSIZE)
        anim = self.get_anim_for_c(ii, jj)
        anim.blit(renderer, (x, y))


    def draw(self, renderer,  level, offset):
        # Currently we dont' rain and snow
        width, height = level.get_size()

        atmosys = level.get_atmospheric_system()

        if atmosys.get_atmospheric_type() == 0:
            return

        walk_map = level.get_walk_map()
        me = level.get_player_manager().get_me()

        d, px, py = me.get_position()

        for i in range(0, 21):
            for j in range(0, 21):

                ii, jj = self.calculate_layer_data_indices(px, py, i, j)

                if not (0 <= ii < width and 0 <= jj < height):
                    continue

                ox = px % 1
                oy = py % 1

                if walk_map[ii][jj] < 1:
                    self.draw_s(i, j, ox, oy, offset, renderer, ii, jj)