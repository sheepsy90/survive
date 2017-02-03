# -*- coding:utf-8 -*-
import pygame
from client.config import CELLSIZE, PLAYER_CENTER_X, PLAYER_CENTER_Y


class BasicBackgroundDrawer():

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager


    def calculate_layer_data_indices(self, px, py, i, j):
        ii = int(px) - PLAYER_CENTER_X + i
        jj = int(py) - PLAYER_CENTER_Y + j

        return ii, jj

    def draw_s(self, i, ii, j, jj, ox, oy, offset, renderer, tile_mapping, lay_to_use_data_of):
        e = lay_to_use_data_of[ii][jj]

        if e == 0:
            return

        resource_key, pos = tile_mapping[e]

        resource_key = resource_key.split(".")[0]
        tsi, tsj = pos
        surface = self.resource_manager.load_image_tile(resource_key, tsi, tsj)
        x = (i + offset) * CELLSIZE - int(ox * CELLSIZE)
        y = (j + offset) * CELLSIZE - int(oy * CELLSIZE)
        rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        renderer.blit(surface, rect)

    def draw(self, renderer, level, offset):
        width, height = level.get_size()
        tile_mapping = level.get_tile_mapping()

        graphics_zorder_layers = level.get_graphcis_zorder_layers()
        graphics_keys = graphics_zorder_layers.keys()
        graphics_keys = sorted(graphics_keys)

        robot_guidance = level.get_robot_guidance_data()
        me = level.get_player_manager().get_me()

        d, px, py = me.get_position()

        for i in range(0, 21):
            for j in range(0, 21):

                ii, jj = self.calculate_layer_data_indices(px, py, i, j)

                if not (0 <= ii < width and 0 <= jj < height):
                    continue


                ox = px % 1
                oy = py % 1

                for key in graphics_keys:
                    current_layer = graphics_zorder_layers[key]
                    self.draw_s(i, ii, j, jj, ox, oy, offset, renderer, tile_mapping, current_layer)
                self.draw_s(i, ii, j, jj, ox, oy, offset, renderer, tile_mapping, robot_guidance)

    def draw_glass_layer(self, renderer, level, offset):
        width, height = level.get_size()
        tile_mapping = level.get_tile_mapping()

        glass_layer_data = level.get_glass_render_data()
        me = level.get_player_manager().get_me()

        d, px, py = me.get_position()

        for i in range(0, 21):
            for j in range(0, 21):

                ii, jj = self.calculate_layer_data_indices(px, py, i, j)

                if not (0 <= ii < width and 0 <= jj < height):
                    continue


                ox = px % 1
                oy = py % 1

                self.draw_s(i, ii, j, jj, ox, oy, offset, renderer, tile_mapping, glass_layer_data)





