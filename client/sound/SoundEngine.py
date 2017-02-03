import os
import pygame
from client.sound.MySound import MySound


class SoundEngine(object):

    def __init__(self):
        self.sound_list = [
            MySound("rain", os.path.abspath("resources/sounds/rain.ogg")),
            MySound("step", os.path.abspath("resources/sounds/footstep.ogg")),
            MySound("search", os.path.abspath("resources/sounds/search.ogg")),
            MySound("backpack_opening", os.path.abspath("resources/sounds/backpack_open.ogg")),
            MySound("backpack_closing", os.path.abspath("resources/sounds/backpack_close.ogg")),
            MySound("alert", os.path.abspath("resources/sounds/alert.ogg")),
            MySound("arcology_ki", os.path.abspath("resources/sounds/arcology_ki.ogg")),
            MySound("rescue_capsule_activated", os.path.abspath("resources/sounds/rescue_capsule_activated.ogg")),
            MySound("not_authorized", os.path.abspath("resources/sounds/not_authorized.ogg")),
            MySound("id_card_required", os.path.abspath("resources/sounds/id_card_required.ogg")),
            MySound("access_granted", os.path.abspath("resources/sounds/access_granted.ogg"))
        ]

        self.sounds = {
            s.get_name(): s for s in self.sound_list
        }

        self.channels = {
            i: pygame.mixer.Channel(i) for i in range(pygame.mixer.get_num_channels())
        }

    def add_to_sound_list(self, my_sound):
        # Check if it still exists
        if my_sound.get_name() not in self.sounds:
            self.sound_list.append(my_sound)
            self.sounds[my_sound.get_name()] = my_sound
            return True

        # If it exists but the path differs then its critical
        if self.sounds[my_sound.get_name()].path == my_sound.path:
            return True

        return False

    def play(self, sound_to_play, single_mode=False):
        """
        This method requests a not busy channel and starts playing the sound if possible
        :param sound_to_play: The key for the sound file to play
        :return: True if the playing could start, False if there was no available channel
        """
        # If we requested single mode for that sound it is only played once
        if single_mode and self.still_playing(sound_to_play):
            return

        channel = pygame.mixer.find_channel()
        if channel is not None:
            channel.play(self.sounds[sound_to_play])
            return True
        else:
            print "[SoundEngine][Warning] Could not start sound because no channel available"
            return False

    def stop(self, sound_to_stop):
        [c.stop() for c in self.channels.values() if c.get_sound() is not None and c.get_sound().get_name() == sound_to_stop]

    def still_playing(self, sound_key):
        currently_active = [channel.get_sound().get_name() for channel in self.channels.values() if channel.get_sound() is not None]
        return sound_key in currently_active

    def play_or_keep_going(self, sound_to_play):
        """ This method should start a sound given by the key when it is not
            played on any channel else just do nothing """
        currently_active = [channel.get_sound().get_name() for channel in self.channels.values() if channel.get_sound() is not None]
        if sound_to_play not in currently_active:
            self.play(sound_to_play)
