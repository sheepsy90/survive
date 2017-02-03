import pygame


class MySound(pygame.mixer.Sound):

    def __init__(self, name, path):
        pygame.mixer.Sound.__init__(self, path)
        self.path = path
        self.name = name

    def get_name(self):
        return self.name

    def __repr__(self):
        return self.name


class MyVoiceActing(MySound):

    def __init__(self, name, path, voice_text):
        MySound.__init__(self, name, path)

        self.voice_text = voice_text

    def get_voice_text(self):
        return self.voice_text
