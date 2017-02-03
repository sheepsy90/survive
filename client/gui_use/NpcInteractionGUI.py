# -*- coding:utf-8 -*-
import pygame
from client.colours import RED, GREEN, BLACK
from client.config import WINDOWHEIGHT, WINDOWWIDTH
from client.drawers.helper import drawText
from client.gui_lib.ButtonGUI import ButtonGUI


class NpcInteractionGUI(object):

    def __init__(self, game_gui_layer, resource_manager, npc_system):
        self.npc_system = npc_system
        self.resource_manager = resource_manager

        self.character_image_cache = {}



        npc_area_width = 700
        npc_area_height = 200
        self.npc_area_rect = pygame.Rect(WINDOWWIDTH/2-npc_area_width/2, WINDOWHEIGHT - npc_area_height, npc_area_width, npc_area_height)
        self.npc_picture_rect = pygame.Rect(WINDOWWIDTH/2-npc_area_width/2, WINDOWHEIGHT - npc_area_height - 98, 98, 98)

        graphics = resource_manager.load_image('layout/gui')
        self.existing_character = graphics.subsurface(pygame.Rect(277, 154, 98, 98))

        offset = 5
        self.border_size = 3
        self.npc_area_text_rect = pygame.Rect(self.npc_area_rect.x + self.border_size + offset,
                                              self.npc_area_rect.y + self.border_size + offset,
                                              self.npc_area_rect.width - 2*(self.border_size + offset),
                                              self.npc_area_rect.height - 2*(self.border_size + offset))
        self.font_for_text = pygame.font.Font('resources/fonts/VENUSRIS.ttf', 16)

        x, y = self.npc_area_rect.topright
        x -= 20
        y -= 20

        self.npc_interaction_close_button = ButtonGUI('dialogue_close', pygame.Rect(x, y, 20, 20),
                                                      caption="X", function=self.close)

        self.npc_interaction_close_button.set_visible(False)
        game_gui_layer.add(self.npc_interaction_close_button)

    def close(self):
        self.npc_system.close()

    def get_character_image(self, npc):
        if npc.get_id() not in self.character_image_cache:
            x, y = npc.get_character_tile_position()
            character_image = self.resource_manager.load_image_tile("characters/characters", x, y, tile_size=98)
            self.character_image_cache[npc.get_id()] = character_image
            return character_image
        return self.character_image_cache[npc.get_id()]

    def draw(self, renderer):
        if self.npc_system.has_current_npc():

            npc = self.npc_system.get_current_npc()

            self.npc_interaction_close_button.set_visible(True)

            character_image = self.get_character_image(npc)

            renderer.fill((255, 255, 255), self.npc_area_rect)
            renderer.blit(character_image, self.npc_picture_rect)

            pygame.draw.rect(renderer, GREEN, self.npc_area_rect, self.border_size)
            pygame.draw.rect(renderer, GREEN, self.npc_picture_rect, self.border_size)

            drawText(renderer, "{}: \"{}\"".format(npc.get_name(), npc.get_text()), BLACK, self.npc_area_text_rect, self.font_for_text)
        else:
            self.npc_interaction_close_button.set_visible(False)
