import json
import logging
import pygame

from client.config import WINDOWWIDTH, WINDOWHEIGHT
from client.sound.MusicEngine import MusicEngine
from client.sound.SoundEngine import SoundEngine
from client.states.AccountCreation import AccountCreation
from client.states.CharacterSelection import CharacterSelection
from client.states.LoginState import LoginState
from client.states.RunningGame import RunningGame


class Client():

    def __init__(self, server_host, server_port):
        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init()

        self.sound_engine = SoundEngine()
        self.music_engine = MusicEngine()
        self.music_engine.set_volume(20)

        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Survive')

        self.states = [
            LoginState("login", self, self.FPSCLOCK, self.DISPLAYSURF, server_host, server_port),
            AccountCreation("account_creation", self, self.FPSCLOCK, self.DISPLAYSURF, server_host, server_port),
            CharacterSelection("character_selection", self, self.FPSCLOCK, self.DISPLAYSURF, server_host, server_port),
            RunningGame("running_game", self, self.FPSCLOCK, self.DISPLAYSURF, self.sound_engine, self.music_engine)
        ]

        self.states = {
            s.name: s for s in self.states
        }

        self.current_state = self.states["login"]
        self.update()

    def transition(self, next_state_name, arguments_as_dict):

        # Because it has a thread we need to completely rebuild it - this needs a general mechanism
        if next_state_name == 'running_game':
            self.states['running_game'] = RunningGame("running_game", self, self.FPSCLOCK, self.DISPLAYSURF,
                                                      self.sound_engine, self.music_engine)

        print "Transition from", next_state_name, "to with args:", arguments_as_dict
        assert next_state_name in self.states, "State was not in the set of states so we can't go there"

        next_state = self.states[next_state_name]
        next_state.enter_state(arguments_as_dict)
        self.current_state.exit_state()
        self.current_state = next_state

    def update(self):
        while True:
            self.current_state.update()



# ########################################
### Start Up Procedure for the client ###
#########################################

if __name__ == '__main__':
    # Fist we need to check which is the login server to talk to
    # This is defined in the configuration file
    with open("configuration.json", "r") as f:
        data = json.loads(f.read())

    logging.basicConfig(format='[%(levelname)s] [%(name)s] %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='client.log',
                        level=logging.INFO)

    # Get the host and the port of the login server
    login_server_host = data["login_server_host"]
    login_server_port = data["login_server_port"]

    client = Client(login_server_host, login_server_port)
