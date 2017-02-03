# -*- coding:utf-8 -*-

from pygame.constants import KEYDOWN, K_LEFT, K_a, K_d, K_w, K_s, K_DOWN, K_UP, K_RIGHT, K_SPACE, K_t, K_ESCAPE, KEYUP, \
    K_c,  K_u


class ClientKeyState():

    def __init__(self):
        self.key_states = {
            "up": 0,
            "down": 0,
            "left": 0,
            "right": 0,
            "search": 0,
            "flashlight": 0,
            "crafting_grid": 0,
            "use": 0
        }

    def set_key_state(self, name, value):
        self.key_states[name] = value

    def get_key_state(self, name):
        return self.key_states[name]


class ClientInputHandler():

    def __init__(self, client_level_manager, sound_engine, client_socket_wrapper):
        self.client_level_manager = client_level_manager
        self.sound_engine = sound_engine
        self.client_socket_wrapper = client_socket_wrapper
        self.client_key_state = ClientKeyState()


    def execute(self, events):
        # Remember the important states before updating them
        searching = self.client_key_state.get_key_state("search")
        flashlight = self.client_key_state.get_key_state("flashlight")
        crafting = self.client_key_state.get_key_state("crafting_grid")
        use = self.client_key_state.get_key_state("use")

        self.__player_input(events)

        direction = self.get_direction_from_key_state()

        if direction is not None:
            self.sound_engine.play_or_keep_going('step')
            self.client_socket_wrapper.send_movment_request(direction)

        if self.client_key_state.get_key_state("flashlight") == 1 and flashlight == 0:
            self.client_level_manager.get_current_level().toggle_flashlight()

        if self.client_key_state.get_key_state("crafting_grid") == 1 and crafting == 0:
            self.client_socket_wrapper.send_open_crafting_container_command()

        if self.client_key_state.get_key_state("search") == 1 and searching == 0:
            self.client_socket_wrapper.send_open_normal_loot_container_command()

        if self.client_key_state.get_key_state("use") == 1 and searching == 0:
            self.client_socket_wrapper.send_client_wants_to_use()

    def __player_input(self, events):
        for event in events:

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    self.client_key_state.set_key_state("left", 1)
                elif event.key == K_RIGHT or event.key == K_d:
                    self.client_key_state.set_key_state("right", 1)
                elif event.key == K_UP or event.key == K_w:
                    self.client_key_state.set_key_state("up", 1)
                elif event.key == K_DOWN or event.key == K_s:
                    self.client_key_state.set_key_state("down", 1)
                elif event.key == K_SPACE:
                    self.client_key_state.set_key_state("search", 1)
                elif event.key == K_t:
                    self.client_key_state.set_key_state("flashlight", 1)
                elif event.key == K_c:
                    self.client_key_state.set_key_state("crafting_grid", 1)
                elif event.key == K_u:
                    self.client_key_state.set_key_state("use", 1)
                elif event.key == K_ESCAPE:
                    exit(0)

            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    self.client_key_state.set_key_state("left", 0)
                elif event.key == K_RIGHT or event.key == K_d:
                    self.client_key_state.set_key_state("right", 0)
                elif event.key == K_UP or event.key == K_w:
                    self.client_key_state.set_key_state("up", 0)
                elif event.key == K_DOWN or event.key == K_s:
                    self.client_key_state.set_key_state("down", 0)
                elif event.key == K_SPACE:
                    self.client_key_state.set_key_state("search", 0)
                elif event.key == K_t:
                    self.client_key_state.set_key_state("flashlight", 0)
                elif event.key == K_c:
                    self.client_key_state.set_key_state("crafting_grid", 0)
                elif event.key == K_u:
                    self.client_key_state.set_key_state("use", 0)
                elif event.key == K_ESCAPE:
                    exit(0)

    def get_direction_from_key_state(self):
        direction = None
        if self.client_key_state.get_key_state("left") == 1:
            direction = (-1, 0)
        elif self.client_key_state.get_key_state("right") == 1:
            direction = (1, 0)
        elif self.client_key_state.get_key_state("up") == 1:
            direction = (0, -1)
        elif self.client_key_state.get_key_state("down") == 1:
            direction = (0, 1)
        return direction