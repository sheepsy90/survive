# -*- coding:utf-8 -*-
import pygame
from pygame.constants import BLEND_RGBA_ADD, BLEND_ADD

from client.colours import BLACK
from client.config import CELLSIZE


class BasicHealthModifierDrawer(object):

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager

        self.type_to_icon_mapping = {
            1: self.resource_manager.load_image_tile('health_icons', 0, 0, tile_size=48), #Toxic
            2: self.resource_manager.load_image_tile('health_icons', 1, 0, tile_size=48), #Vomit
            3: self.resource_manager.load_image_tile('health_icons', 2, 0, tile_size=48), #Gas
            4: self.resource_manager.load_image_tile('health_icons', 3, 0, tile_size=48), #Undef

            5: self.resource_manager.load_image_tile('health_icons', 0, 1, tile_size=48), #Thirst-
            6: self.resource_manager.load_image_tile('health_icons', 1, 1, tile_size=48), #Hunger-
            7: self.resource_manager.load_image_tile('health_icons', 2, 1, tile_size=48), #Thirst+
            8: self.resource_manager.load_image_tile('health_icons', 3, 1, tile_size=48), #Hunger+

            301: self.resource_manager.load_image_tile('health_icons', 0, 2, tile_size=48), # Simple Damage
            302: self.resource_manager.load_image_tile('health_icons', 1, 2, tile_size=48), # Simple Shocked
            11: self.resource_manager.load_image_tile('health_icons', 2, 2, tile_size=48),
            12: self.resource_manager.load_image_tile('health_icons', 3, 2, tile_size=48),

            13: self.resource_manager.load_image_tile('health_icons', 0, 3, tile_size=48),
            14: self.resource_manager.load_image_tile('health_icons', 1, 3, tile_size=48),
            15: self.resource_manager.load_image_tile('health_icons', 2, 3, tile_size=48),
            16: self.resource_manager.load_image_tile('health_icons', 3, 3, tile_size=48)
        }

    def draw_health_icon_element_at(self, mod, count, renderer, logical_x, logical_y):
        assert logical_x == 0 or logical_x == 1
        real_x = 8+48*logical_x
        real_y = 117+48*logical_y

        # The icon draw part
        surface = self.type_to_icon_mapping[mod]
        rect = pygame.Rect(real_x, real_y, CELLSIZE, CELLSIZE)

        # The count draw part
        font = pygame.font.Font('freesansbold.ttf', 12)
        stack_size_text = font.render(str(count), True, (0, 0, 0))

        text_rect = stack_size_text.get_rect()
        text_rect.center = (real_x+48-10, real_y+48-10)

        renderer.blit(surface, rect)
        renderer.blit(stack_size_text, text_rect)


    def draw(self, renderer, level):

        hm = level.get_health_modifier_manager()

        mods = hm.get_health_mods()

        logical_counter = 0
        for mod in mods:

            lx, ly = logical_counter % 2, logical_counter/2

            self.draw_health_icon_element_at(mod, mods[mod], renderer, lx, ly)
            logical_counter += 1



