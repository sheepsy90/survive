# -*- coding:utf-8 -*-

import pygame
from client.colours import BLACK
from client.drawers.helper import dim, blurSurf
from common.constants.ServerToClientNetworkCommands import LOOK_RIGHT, LOOK_LEFT, LOOK_DOWN, LOOK_UP
from client.config import CELLSIZE, PLAYER_CENTER_X, PLAYER_CENTER_Y


class BasicPlayerDrawer():

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.player_image_left = self.resource_manager.load_image_tile('players', 0, 1)
        self.player_image_right = self.resource_manager.load_image_tile('players', 0, 0)
        self.player_image_up = self.resource_manager.load_image_tile('players', 0, 2)
        self.player_image_down = self.resource_manager.load_image_tile('players', 1, 2)
        self.player_image = self.resource_manager.load_image_tile('players', 0, 0)

    def get_player_img_based_on_look_direction(self, direction):
        if direction == LOOK_RIGHT:
            player_img = self.player_image_right.copy()
        elif direction == LOOK_LEFT:
            player_img = self.player_image_left.copy()
        elif direction == LOOK_DOWN:
            player_img = self.player_image_down.copy()
        elif direction == LOOK_UP:
            player_img = self.player_image_up.copy()
        else:
            player_img = self.player_image.copy()
        return player_img

    def get_player_anim_based_on_look_direction(self, direction):
        total = 0.5
        if direction == LOOK_RIGHT:
            player_img = self.resource_manager.load_animation("animations/walk_anim_player_right", 4, [total/4 for i in range(4)])
        elif direction == LOOK_LEFT:
            player_img = self.resource_manager.load_animation("animations/walk_anim_player_left", 4, [total/4 for i in range(4)])
        elif direction == LOOK_DOWN:
            player_img = self.resource_manager.load_animation("animations/walk_anim_player_down", 4, [total/4 for i in range(4)])
        elif direction == LOOK_UP:
            player_img = self.resource_manager.load_animation("animations/walk_anim_player_up", 4, [total/4 for i in range(4)])
        else:
            player_img = self.player_image.copy()
        return player_img


    def draw_players(self, renderer, level, offset):
        """ This method is responsible for drawing players from the level object """

        players = level.get_player_manager().get_players()

        me = level.get_player_manager().get_me()

        d, px, py = me.get_position()

        for player in players:

            if player == me:

                direction, posx, posy = player.get_position()
                name = player.get_name()

                x = (offset + PLAYER_CENTER_X) * CELLSIZE
                y = (offset + PLAYER_CENTER_Y) * CELLSIZE
                rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)

                name_tag_font = pygame.font.Font('freesansbold.ttf', 16)
                name_tag = name_tag_font.render(name, True, BLACK)
                name_tag_rect = name_tag.get_rect()
                name_tag_rect.center = (x + CELLSIZE / 2, y - CELLSIZE / 2)

                if player.is_moving():
                    player_anim = self.get_player_anim_based_on_look_direction(direction)
                    player_anim.play(player.get_moving_timer())
                    player_anim.blit(renderer, (rect.x, rect.y))
                else:
                    player_img = self.get_player_img_based_on_look_direction(direction)
                    renderer.blit(player_img, rect)


                renderer.blit(name_tag, name_tag_rect)
            else:
                direction, posx, posy = player.get_position()

                dx = posx - px
                dy = posy - py

                if -11 <= dx <= 11 and -11 <= dy <= 11:
                    dx = dx + 9
                    dy = dy + 9

                    x = (dx + offset) * CELLSIZE
                    y = (dy + offset) * CELLSIZE
                    rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)

                    if player.is_moving():
                        player_anim = self.get_player_anim_based_on_look_direction(direction)
                        player_anim.play(player.get_moving_timer())
                        player_anim.blit(renderer, (rect.x, rect.y))
                    else:
                        player_img = self.get_player_img_based_on_look_direction(direction)
                        renderer.blit(player_img, rect)

    def change_screen_based_on_health(self, renderer, level):
        me = level.get_player_manager().get_me()
        bluriness, redness = me.get_health_properties()
        renderer = blurSurf(renderer, bluriness)
        dim(renderer, darken_factor=redness, color_filter=(255, 0, 0))
        return renderer
