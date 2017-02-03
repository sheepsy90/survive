import random
import pygame
import time
from pygame.surface import Surface
from client.colours import BLACK
from client.config import WINDOWHEIGHT, WINDOWWIDTH


class PhotoBackgroundSystem():

    def __init__(self, resource_manager):

        photo_set = [
            resource_manager.load_image("startscreen/forestfire"),
            resource_manager.load_image("startscreen/orca"),
            resource_manager.load_image("startscreen/oiledbird"),
            resource_manager.load_image("startscreen/riotpolice"),
            resource_manager.load_image("startscreen/fskpf"),
            resource_manager.load_image("startscreen/oilonsea"),
            resource_manager.load_image("startscreen/hurrican"),
            resource_manager.load_image("startscreen/deforestation"),
            resource_manager.load_image("startscreen/landfill"),
            resource_manager.load_image("startscreen/oilspill"),
            resource_manager.load_image("startscreen/whales"),
            resource_manager.load_image("startscreen/plant"),
            resource_manager.load_image("startscreen/acidrainwoods"),
        ]

        random.shuffle(photo_set)
        photo_set = photo_set[:int(len(photo_set)*0.75)]

        #3030, 9119
        seed = random.randint(0, 10000)
        print "Seed", seed
        random.seed(seed)

        self.image_positions = [
            [random.randint(int(0.1*WINDOWWIDTH), WINDOWWIDTH*0.9) - f.get_rect().width / 2,
             random.randint(int(-0.1 * WINDOWHEIGHT), WINDOWHEIGHT - f.get_rect().height / 2),
             pygame.transform.rotate(f, random.gauss(0, 10)).convert()] for f in photo_set
        ]

        random.shuffle(self.image_positions)

        for e in self.image_positions:
            sf = e[2]
            sf.set_colorkey((255,128,0, 255))

        start_time = time.time()
        self.duration = 2.2
        self.start_distance = 3.4

        self.start_time = [start_time + e for e in range(len(self.image_positions))]
        self.end_time = [start_time + self.start_distance*e + self.duration for e in range(len(self.image_positions))]

        self.d = 0

    def draw(self, renderer):
        surface = Surface((WINDOWWIDTH, WINDOWHEIGHT))
        #surface.convert_alpha(surface)
        surface.fill(BLACK)
        #surface.set_alpha(128)

        self.d += 1
        self.d %= 255

        #x, y, f = self.image_positions[0]
        #f.set_alpha(self.d)
        #renderer.blit(f, pygame.Rect(x, y, 1, 1))



        current = time.time()
        for idx in range(len(self.image_positions)):
            image = self.image_positions[idx]
            start = self.start_time[idx]
            end = self.end_time[idx]
            x, y, f = image

            if start <= current <= end:
                percent_alpha = (end - current) / self.duration
                percent_alpha = 255 - percent_alpha*255
                percent_alpha = int(percent_alpha)
                f_c = f.copy()
                f_c.set_alpha(percent_alpha)


                surface.blit(f_c, (x, y))

            if current > end:
                surface.blit(f, pygame.Rect(x, y, 1, 1))


        renderer.blit(surface, pygame.Rect(0, 0, 1, 1))