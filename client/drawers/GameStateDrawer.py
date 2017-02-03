# -*- coding:utf-8 -*-
import pygame
import random
from client.colours import BLACK
from client.config import CELLSIZE
from client.drawers.BasicAtmosphericDrawer import BasicAtmosphericDrawer
from client.drawers.BasicBackgroundDrawer import BasicBackgroundDrawer
from client.drawers.BasicEffectDrawer import BasicEffectDrawer
from client.drawers.BasicEnemyDrawer import BasicEnemyDrawer
from client.drawers.BasicLightDrawer import BasicLightDrawer
from client.drawers.BasicMarkerDrawer import BasicMarkerDrawer
from client.drawers.BasicObjectDrawer import BasicObjectDrawer
from client.drawers.BasicPlayerDrawer import BasicPlayerDrawer


class GameStateDrawer():
    """ This is the special layer which is responsible for drawing the game state """

    def __init__(self, client_level_manager, resource_manager, maker_logic, tsm, camera_shaker, state_machine, effect_list):
        game_DRAW_layer_width = 20*CELLSIZE
        game_DRAW_layer_height = 20*CELLSIZE

        self.layer_surface = pygame.Surface((game_DRAW_layer_width, game_DRAW_layer_height))

        self.client_level_manager = client_level_manager
        self.resource_manager = resource_manager
        self.marker_logic = maker_logic

        self.basic_background_drawer = BasicBackgroundDrawer(self.resource_manager)
        self.basic_object_drawer = BasicObjectDrawer(self.resource_manager)
        self.basic_player_drawer = BasicPlayerDrawer(self.resource_manager)
        self.basic_enemy_drawer = BasicEnemyDrawer(self.resource_manager)
        self.basic_light_drawer = BasicLightDrawer()
        self.basic_atmospheric_drawer = BasicAtmosphericDrawer(self.resource_manager)
        self.basic_marker_drawer = BasicMarkerDrawer(self.resource_manager, self.marker_logic)
        self.basic_effect_drawer = BasicEffectDrawer(effect_list)

        self.tsm = tsm
        self.camera_shaker = camera_shaker
        self.state_machine = state_machine

    def draw(self):
        # Get the current level
        current_level = self.client_level_manager.get_current_level()

        if current_level is None:
            return

        # First get the width and height of the level
        width, height = current_level.get_size()

        # Make sure we only draw things if we have a level boundary
        if height is None or width is None:
            return

        #self.layer_surface = self.layer_surface.convert_alpha()

        # Define the number of surrounded 'boundary tiles'
        offset = 0

        self.layer_surface.fill(BLACK)

        self.basic_background_drawer.draw(self.layer_surface, current_level, offset)
        self.basic_effect_drawer.draw(self.layer_surface, current_level, offset)
        self.basic_object_drawer.draw(self.layer_surface, current_level, offset)
        self.basic_enemy_drawer.draw(self.layer_surface, current_level, offset)
        self.basic_player_drawer.draw_players(self.layer_surface, current_level, offset)
        self.basic_light_drawer.draw(self.layer_surface, current_level, offset)
        self.basic_atmospheric_drawer.draw(self.layer_surface, current_level, offset)
        self.basic_marker_drawer.draw(self.layer_surface, current_level, offset)
        self.basic_background_drawer.draw_glass_layer(self.layer_surface, current_level, offset)

        if self.state_machine.is_character_still_tutorial():
            self.tsm.current_state()

            self.camera_shaker.perform(self.layer_surface)

            if random.random() > 0.995 and not self.camera_shaker.is_camera_shaking():
                self.camera_shaker.start_shaking()

        #self.layer_surface = self.basic_player_drawer.change_screen_based_on_health(self.layer_surface, current_level)



