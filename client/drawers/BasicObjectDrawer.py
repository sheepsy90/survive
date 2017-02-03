# -*- coding:utf-8 -*-
import pygame
import random
import math
from pygame.constants import BLEND_RGBA_SUB
from client.colours import RED, GREEN

from client.config import CELLSIZE
import time

class BasicObjectDrawer():

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.manhatten_radius = 11

    def draw(self, renderer, level, offset):
        objects = level.get_object_manager().get_objects()
        stepable_values = level.get_object_manager().get_stepable_values()

        me = level.get_player_manager().get_me()
        d, posx, posy = me.get_position()

        mov_adder_x = 0
        mov_adder_y = 0

        if me.is_moving():
            if d ==1 or d == 2:
                mov_adder_x += 1
            else:
                mov_adder_y += 1

        for obj in objects:
            if not obj.is_visible():
                continue


            epx, epy = obj.get_position()

            dx = epx - (posx)*CELLSIZE
            dy = epy - (posy+1)*CELLSIZE

            if -self.manhatten_radius*CELLSIZE <= dx <= (self.manhatten_radius)*CELLSIZE \
                    and -self.manhatten_radius*CELLSIZE <= dy <= (self.manhatten_radius)*CELLSIZE:
                dx = dx + 9*CELLSIZE
                dy = dy + 9*CELLSIZE




                tk, tsi, tsj = obj.get_tileset_infos()

                world_object_id = obj.get_object_id()
                if world_object_id in stepable_values:
                    state = stepable_values[world_object_id]
                    if state:
                        tsi += 1

                surface = self.resource_manager.load_image_tile(tk, tsi, tsj)
                x = dx + offset * CELLSIZE + mov_adder_x
                y = dy + offset * CELLSIZE + mov_adder_y


                if obj.has_payload():
                    self.hanlde_mine_drawing(obj, renderer, x, y, offset, posx, posy)

                rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
                renderer.blit(surface, rect)

                # TODO if the objects runs out of sight the laser should not
                if obj.has_payload():
                    self.hanlde_laser_drawing(obj, renderer, x, y, offset, posx, posy)

    def hanlde_laser_drawing(self, obj, renderer, x, y,  offset, posx, posy):
        payload = obj.get_payload()

        if u'LASER_COMPONENT' in payload:
            active = int(payload[u'LASER_COMPONENT']["active"])

            if active:
                distance = int(payload[u'LASER_COMPONENT']["distance"])
                direction = payload[u'LASER_COMPONENT']["direction"]

                if direction == "DOWN":
                    x_s = int(x + CELLSIZE/2)
                    y_start = y + 16

                    # We need to calculate the logical end point dependend on the player position
                    end_y = y + (distance * CELLSIZE) + 16

                    surf = pygame.Surface((3, (end_y - y_start)))
                    alp = random.randint(80, 130)
                    red = random.randint(210, 255)
                    surf.fill((red, 0, 0, alp))
                    surf.set_alpha(alp)

                    renderer.blit(surf, (x_s-2, y_start))
                if direction == "RIGHT":
                    x_start = int(x + CELLSIZE/2) + 7
                    y_start = y + 8

                    # We need to calculate the logical end point dependend on the player position
                    end_x = x + (distance * CELLSIZE)

                    surf = pygame.Surface(((end_x - x_start), 3))
                    alp = random.randint(80, 130)
                    red = random.randint(210, 255)
                    surf.fill((red, 0, 0, alp))
                    surf.set_alpha(alp)

                    renderer.blit(surf, (x_start-2, y_start))


    def hanlde_mine_drawing(self, obj, renderer, x, y,  offset, posx, posy):
        payload = obj.get_payload()

        if u'MINE_COMPONENT' in payload:
            radius = int(payload[u'MINE_COMPONENT']["radius"])

            dx = x + CELLSIZE/2
            dy = y + CELLSIZE/2
            THICKNESS = 5
            STRETCH = 0.5


            for i in range(radius+2):

                fake_radius = (((i/float(radius))+(time.time()*0.8)) % radius)*CELLSIZE
                image = pygame.Surface([fake_radius*2, int(STRETCH*fake_radius*2)], pygame.SRCALPHA, 32)
                image = image.convert_alpha()


                if fake_radius*STRETCH > THICKNESS:
                    pygame.draw.ellipse(image, (255, 0, 0, max(0, 200-fake_radius*3)), pygame.Rect(0, 0, fake_radius*2, (STRETCH*fake_radius*2)), THICKNESS)

                renderer.blit(image, pygame.Rect(dx - fake_radius, dy - int(STRETCH*fake_radius), fake_radius*2, int(STRETCH*fake_radius*2)))

            """
            num_pulse = 7
            mod = 3
            for i in range(7):
                h = time.time()
                result = (h + ((mod*float(i))/num_pulse)) % mod


                from_to = result / 3.0
                y_intermediate = int(y_start + int((end_y - y_start)*from_to))

                surf2 = pygame.Surface((5, 5))
                surf2.fill((255, 0, 0, 100))
                surf2.set_alpha(100)

                renderer.blit(surf2, (x_s-3, y_intermediate))
            """

