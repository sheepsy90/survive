# -*- coding:utf-8 -*-

import pygame
import math
from pygame.constants import BLEND_RGBA_SUB
from pygame.rect import Rect
from client.config import CELLSIZE


class BasicLightDrawer():

    def draw_inverse_circle(self, screen, width, height, color, center, radius, n):
        left = center[0] - radius
        right = center[0] + radius
        top = center[1] - radius
        bottom = center[1] + radius
        screen_width = width
        screen_height = height

        # make an inverse square
        pygame.draw.rect(screen, color, Rect(0, 0, left, screen_height))
        pygame.draw.rect(screen, color, Rect(right, 0, screen_width - right, screen_height))
        pygame.draw.rect(screen, color, Rect(left, 0, right - left, top))
        pygame.draw.rect(screen, color, Rect(left, bottom, right - left, screen_height - bottom))

        #fill in the corners with pretty roundness

        # list of numbers, 0 through n - 1
        points = range(0, n)

        # list of n numbers evenly distributed from 0 to 1.0 inclusive
        points = map(lambda pt: pt / (len(points) - 1.0), points)

        # list of n radians evenly distributed from 0 to pi/4 inclusive
        points = map(lambda pt: pt * 3.1415926535 * 2  / 4, points)

        # list of points evenly distributed around the circumference in the first quadrant of a unit circle
        points = map(lambda pt: (math.cos(pt), math.sin(pt)), points)

        # list of points evenly distributed around the circumference of the circle of desired size centered on the origin
        points = map(lambda pt: (radius * pt[0], radius * pt[1]), points)

        # we'll draw these points with trapezoids that connect to the
        # top or bottom rectangle and flip them around each quadrant
        for quadrant in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
            x_flip = quadrant[0]
            y_flip = quadrant[1]
            edge = center[1] + radius * y_flip
            for i in xrange(len(points) - 1):
                A = (points[i][0] * x_flip + center[0], points[i][1] * y_flip + center[1])
                B = (points[i + 1][0] * x_flip + center[0], points[i + 1][1] * y_flip + center[1])
                A_edge = (A[0], edge)
                B_edge = (B[0], edge)

                pygame.draw.polygon(screen, color, (A, B, B_edge, A_edge))

    def draw(self, renderer, level, offset):

        atmosys = level.get_atmospheric_system()

        # Get the current daylight level
        if atmosys.get_atmospheric_type() == 0:
            daylight_alpha = 0
        else:
            daylight_alpha = 40

        # Create the surface we draw on
        game_area_surface = pygame.Surface((704, 704))

        # Create the color we are using for drawing
        light_color = (daylight_alpha, daylight_alpha, daylight_alpha)

        # Determine the radius of the light around the player
        if level.flashlight_enabled() and daylight_alpha > 0:
            lightradius = 52
        else:
            lightradius = 0

        if lightradius == 0:
            # Safe computation time when there is no circle to be drawn
            self.draw_inverse_circle(game_area_surface, 704, 704, light_color, (0, 0), lightradius, 0)
        else:
            # Get the player position
            player = level.get_player_manager().get_me()
            me = level.get_player_manager().get_me()

            # Calculate the concrete coordinates
            if player is not None:
                d, i, j = player.get_position()
                x = (9 + offset) * CELLSIZE + CELLSIZE/2
                y = (9 + offset) * CELLSIZE + CELLSIZE/2

                # Shadow all except the circle
                self.draw_inverse_circle(game_area_surface, 704, 704, light_color, (x, y), lightradius, 32)


        # Apply the surface on the graphics renderer
        renderer.blit(game_area_surface, (0, 0), special_flags=BLEND_RGBA_SUB)