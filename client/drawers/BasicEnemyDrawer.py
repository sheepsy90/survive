# -*- coding:utf-8 -*-
import pygame

import random
import time
from client.colours import RED, GREY, BLACK, ROSE, YELLOW
from client.config import CELLSIZE


class BasicEnemyDrawer(object):

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.animations = {}
        self.destroy_animations = {}

        self.shock_anim_duration = 1.4
        self.shock = self.resource_manager.load_animation("animations/shock_enemy_animation", 6, [self.shock_anim_duration/6 for i in range(6)], tile_size= 96)
        self.shock.play()

    def check_destroy_animation(self, id, started):
        if id not in self.destroy_animations:
            self.destroy_animations[id] = self.resource_manager.load_animation("vacuum_cleaner_destroy", 7, [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], loop=False)
            self.destroy_animations[id].play(time.time())
        return self.destroy_animations[id]

    def check_enemy_animation(self, id):
        if id not in self.animations:
            self.animations[id] = self.resource_manager.load_animation("vacuum_cleaner", 7, [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], loop=True)
            self.animations[id].play(time.time() + random.random())
        return self.animations[id]

    def draw(self, renderer, level, offset):
        me = level.get_player_manager().get_me()

        d, px, py = me.get_position()

        enemy_manager = level.get_client_enemy_manager()
        destroyed = enemy_manager.get_destroyed()
        attacking_enemies = enemy_manager.get_enemies_attacking()

        remove_enemy = []
        for enemy in enemy_manager.get_enemies():
            enemy_id, d, i, j, current_life, max_life = enemy

            dx = i - px
            dy = j - py

            if -11 <= dx <= 11 and -11 <= dy <= 11:
                dx = dx + 9
                dy = dy + 9

                x = (dx + offset) * CELLSIZE
                y = (dy + offset) * CELLSIZE

                x = int(x)
                y = int(y)

                if enemy_id in destroyed:
                    # We need to play the in destruction animation
                    if time.time() - destroyed[enemy_id] < 2:
                        anim = self.check_destroy_animation(enemy_id, destroyed[enemy_id])
                        anim.blit(renderer, (x, y))
                    else:
                        remove_enemy.append(enemy_id)
                else:

                    if enemy_id in attacking_enemies:
                        start_time = attacking_enemies[enemy_id]
                        delta = time.time() - start_time
                        if delta < self.shock_anim_duration:
                            self.shock.play()
                            self.shock.blit(renderer, (x - 32, y - 26))
                        else:
                            enemy_manager.remove_attacking_enemy(enemy_id)

                    anim = self.check_enemy_animation(enemy_id)
                    anim.blit(renderer, (x, y))

                    percent_life = current_life/float(max_life)
                    percent_life = int(percent_life*32)

                    renderer.fill(GREY, pygame.Rect(x, y, 32, 4))
                    renderer.fill(RED, pygame.Rect(x, y, percent_life, 4))
                    pygame.draw.rect(renderer, BLACK, pygame.Rect(x, y, 32, 4), 1)

        bm = level.get_bullet_manager()
        active, in_destruction = bm.get_bullet_infos()


        remove_them = []
        for b_id in active:
            i, j = active[b_id]

            dx = i - px
            dy = j - py

            if -11 <= dx <= 11 and -11 <= dy <= 11:
                dx = dx + 9
                dy = dy + 9

                x = (dx + offset) * CELLSIZE + CELLSIZE/2
                y = (dy + offset) * CELLSIZE + CELLSIZE/2

                x = int(x)
                y = int(y)

                if b_id in in_destruction:
                    # We need to play the in destruction animation
                    if time.time() - in_destruction[b_id] < 0.5:
                        # TODO play sound and do other stuff
                        pass
                    else:
                        remove_them.append(b_id)
                else:
                    # Just update the bullet
                    pygame.draw.circle(renderer, RED, (x, y), 2)

        for id in remove_them:
            bm.remove_bullet(id)