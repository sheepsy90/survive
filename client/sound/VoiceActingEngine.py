# -*- coding:utf-8 -*-

import os
import pygame
from pygame.rect import Rect
from client.colours import WHITE
from client.config import WINDOWHEIGHT, WINDOWWIDTH
from client.sound.MySound import MyVoiceActing


class VoiceActingEngine():


    def __init__(self, sound_engine):
        self.sound_engine = sound_engine
        self.titleFont = pygame.font.Font('freesansbold.ttf', 24)
        self.font_height = self.titleFont.size("Tg")[1]*2

        self.voice_actings = [
            MyVoiceActing("tutorial_9", os.path.abspath("resources/voiceacting/tutorial_9.ogg"),
                          voice_text="The status tells me that it is back to normal. Now I can start it."),

            MyVoiceActing("tutorial_8", os.path.abspath("resources/voiceacting/tutorial_8.ogg"),
                          voice_text="Perfect. Now I take this in my hands <RMB> and use it with the capsule. "
                                     "That should do it."),

            MyVoiceActing("tutorial_7", os.path.abspath("resources/voiceacting/tutorial_7.ogg"),
                          voice_text="The electronics are in here - but i need to assemble them <c>."),

            MyVoiceActing("tutorial_6", os.path.abspath("resources/voiceacting/tutorial_6.ogg"),
                          voice_text="That did not work. Something with the electronics. "
                                     "Maybe there is a replacement near the robot supply cabinet."),

            MyVoiceActing("tutorial_5", os.path.abspath("resources/voiceacting/tutorial_5.ogg"),
                          voice_text="This is the thing. I hope it still works. <interact with u>"),

            MyVoiceActing("tutorial_4", os.path.abspath("resources/voiceacting/tutorial_4.ogg"),
                          voice_text="Now I should really get out of here. The rescue capsule is on the balcony."),

            MyVoiceActing("tutorial_3", os.path.abspath("resources/voiceacting/tutorial_3.ogg"),
                          voice_text="I should wear the mask immediately. The rest I just take with me."
                                     " <Open Backpack and Drag/Drop Items, Right Click for wearing>"),

            MyVoiceActing("tutorial_2", os.path.abspath("resources/voiceacting/tutorial_2.ogg"),
                          voice_text="This is the cabinet. It must be in here. <space>"),

            MyVoiceActing("tutorial_1", os.path.abspath("resources/voiceacting/tutorial_1.ogg"),
                          voice_text="Quick. I need to find the rescue kit. It is probably in the entrance room.")
        ]

        self.voice_acting_texts = {
            e.get_name(): e.get_voice_text() for e in self.voice_actings
        }

        for element in self.voice_actings:
            if not self.sound_engine.add_to_sound_list(element):
                raise KeyError("Duplicated Key for Sound")

        self.voice_acting_active = False
        self.current_active_voice_acting_key = None

    def perform_voice_acting(self, voice_acting_key):
        """ This method starts a voice acting process """
        if not self.voice_acting_active:
            self.sound_engine.play(voice_acting_key)
            self.voice_acting_active = True
            self.current_active_voice_acting_key = voice_acting_key

    def update(self, renderer):
        """ This method draws the corresponding Text onto the screen as long as the voice acting is running """
        if self.voice_acting_active:
            if self.sound_engine.still_playing(self.current_active_voice_acting_key):
                self.drawText(renderer, self.voice_acting_texts[self.current_active_voice_acting_key], WHITE, (32, WINDOWHEIGHT-self.font_height-10, WINDOWWIDTH-32, self.font_height), self.titleFont)
            else:
                self.current_active_voice_acting_key = None
                self.voice_acting_active = False

    def still_active(self, voice_key):
        if self.voice_acting_active and self.current_active_voice_acting_key == voice_key:
            return True
        return False


    # draw some text into an area of a surface
    # automatically wraps words
    # returns any text that didn't get blitted
    def drawText(self, surface, text, color, rect, font, aa=True, bkg=None):

        rect = Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text