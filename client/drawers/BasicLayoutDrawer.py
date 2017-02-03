# -*- coding:utf-8 -*-
import pygame
import math


class OwnSurface():

    def __init__(self, surface):
        self.surface = surface
        self.rect = surface.get_rect()

    def draw_at(self, renderer, x, y):
        renderer.blit(self.surface, pygame.Rect(x, y, self.rect.width, self.rect.height))


class BasicLayoutDrawer(object):

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager

        self.graphics = self.resource_manager.load_image('layout/gui')

        # The Elements for the left side of the screen
        self.top_left_corner = OwnSurface(self.graphics.subsurface(pygame.Rect(0, 0, 147, 117)))
        self.health_status_element_row = OwnSurface(self.graphics.subsurface(pygame.Rect(0, 117, 112, 48)))
        self.health_status_element_row_ending = OwnSurface(self.graphics.subsurface(pygame.Rect(0, 165, 112, 8)))

        # The Elements for the right side of the screen
        self.abstract_control_element = OwnSurface(self.graphics.subsurface(pygame.Rect(164, 0, 75, 75)))
        self.container_open_marker_element = OwnSurface(self.graphics.subsurface(pygame.Rect(148, 0, 15, 39)))

        self.space_element = OwnSurface(self.graphics.subsurface(pygame.Rect(164, 75, 75, 75)))


    def get_health_mods_count(self, level):
        hm = level.get_health_modifier_manager()
        mods = hm.get_health_mods()
        return len(mods)

    def draw_left_side_screen(self, level, renderer):
        # Determine how many health icons there are to draw
        hm_count = self.get_health_mods_count(level)
        # Draw the Top Level GUI Which shows the character
        self.top_left_corner.draw_at(renderer, 0, 0)

        for i in range(int(math.ceil(hm_count / 2.))):
            self.health_status_element_row.draw_at(renderer, 0, 117 + 48 * i)

        if hm_count == 0:
            self.health_status_element_row_ending.draw_at(renderer, 0, 117)
        else:
            self.health_status_element_row_ending.draw_at(renderer, 0, 117 + 48 * (i + 1))

    def draw(self, renderer, level):
        self.draw_left_side_screen(level, renderer)
        self.draw_right_side_screen(renderer)

    def draw_right_side_screen(self, renderer):

        current_surface = pygame.display.get_surface()
        current_surface_rect = current_surface.get_rect()

        sf_w, sf_h = current_surface_rect.width, current_surface_rect.height

        self.abstract_control_element.draw_at(renderer, sf_w-75, 0)
        self.space_element.draw_at(renderer, sf_w-75, 75)
        self.space_element.draw_at(renderer, sf_w-75, 150)
        self.abstract_control_element.draw_at(renderer, sf_w-75, 225)
        self.space_element.draw_at(renderer, sf_w-75, 300)
        self.space_element.draw_at(renderer, sf_w-75, 375)
        self.abstract_control_element.draw_at(renderer, sf_w-75, 450)

        self.container_open_marker_element.draw_at(renderer, sf_w-90, 0)
        self.container_open_marker_element.draw_at(renderer, sf_w-90, 225)
        self.container_open_marker_element.draw_at(renderer, sf_w-90, 450)


