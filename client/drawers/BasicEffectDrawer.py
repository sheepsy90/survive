# -*- coding:utf-8 -*-
import pygame
import time
from client.colours import RED, BLACK

from client.config import CELLSIZE


class EffectObject():

    def __init__(self, x, y, start_time, duration):
        self.x = x
        self.y = y
        self.start_time = start_time
        self.duration = duration

        self.end_time = start_time + duration

    def is_active(self, current_time):
        return current_time < self.end_time

    def get_position(self):
        return self.x, self.y


class GuardDenysEffect(EffectObject):

    def __init__(self, guard_obj_id, x, y):
        EffectObject.__init__(self, x, y, time.time(), 2)


class EffectList():

    def __init__(self):
        self.list_of_effects = []

    def __add__(self, other):
        self.list_of_effects.append(other)

    def get_active_effects(self, current_time):
        return [e for e in self.list_of_effects if e.is_active(current_time)]

    def clean(self, current_time):
        self.list_of_effects = [e for e in self.list_of_effects if e.is_active(current_time)]


class BasicEffectDrawer():

    def __init__(self, effect_stack):
        self.effect_stack = effect_stack

        self.manhattan_radius = 11
        self.drawing_radius = self.manhattan_radius * CELLSIZE

    def is_in_draw_range(self, player_position, object_position):
        opx, opy = object_position
        ppx, ppy = player_position

        dx = CELLSIZE*opx - ppx * CELLSIZE
        dy = CELLSIZE*opy - ppy * CELLSIZE

        if -self.drawing_radius <= dx <= self.drawing_radius and -self.drawing_radius <= dy <= self.drawing_radius:
            dx += 9 * CELLSIZE
            dy += 9 * CELLSIZE
            return True, (dx, dy)
        else:
            return False, ()

    def draw(self, renderer, level, offset):
        # First we need the position of the player so we can calculate the relative position
        me = level.get_player_manager().get_me()
        direction, pos_x, pos_y = me.get_position()
        player_position = (pos_x, pos_y)

        current_time = time.time()

        # Clean up the effect stack - remove outdated elements
        self.effect_stack.clean(current_time)

        active_effects = self.effect_stack.get_active_effects(current_time)

        for effect in active_effects:
            effect_position = effect.get_position()

            in_draw_range, dxdy = self.is_in_draw_range(player_position, effect_position)

            if in_draw_range:
                dx, dy = dxdy
                x = dx + offset * CELLSIZE
                y = dy + offset * CELLSIZE

                if isinstance(effect, GuardDenysEffect):
                    rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
                    pygame.draw.rect(renderer, RED, rect)
                else:
                    rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
                    pygame.draw.rect(renderer, BLACK, rect)
