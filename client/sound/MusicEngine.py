# -*- coding:utf-8 -*-

import os
import pygame


class MusicEngine():

    def __init__(self):
        pygame.mixer.music.load(os.path.abspath("resources/music/progress.mp3"))
        pygame.mixer.music.play()

    def set_volume(self, volume):
        """ Volume from [0, 100] """
        pygame.mixer.music.set_volume(volume / 100.0)

    def get_volume(self):
        """ Volume from [0, 100] """
        return int(100 * pygame.mixer.music.get_volume())