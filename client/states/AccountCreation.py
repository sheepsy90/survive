import pygame
import time
from pygame.constants import KEYDOWN, KEYUP, K_ESCAPE
from client.colours import BGCOLOR, RED, BLACK
from client.config import WINDOWWIDTH, WINDOWHEIGHT, FPS
from client.drawers.helper import draw_text_on_screen_at
from client.gui_lib.ButtonGUI import ButtonGUI
from client.gui_lib.GUILayer import GUILayer
from client.gui_lib.PasswordTextGUI import PasswordTextGUI
from client.gui_lib.TextGUI import TextGUI
from client.network.LoginServiceClient import LoginServerClient, AccountResponse
from client.sound.ResourceManager import ResourceManager
from client.states.State import State


class ErrorMessageDrawer(object):

    def __init__(self, y):
        self.y = y

        self.error_messages = []
        self.active = False
        self.render_error_start_time = None

    def add(self, message, duration):
        self.error_messages.append([message, duration])

    def draw(self, renderer):
        if not self.active and len(self.error_messages) > 0:
            self.active = True
            self.render_error_start_time = time.time()

        if self.active:
            message, duration = self.error_messages[0]

            delta = (time.time() - self.render_error_start_time) / duration
            delta = delta ** 2
            delta = 255 - int(delta * 255)
            delta = max(0, delta)
            draw_text_on_screen_at(renderer, message,
                                   WINDOWWIDTH / 2, self.y, 32, c1=RED, c2=BLACK, alpha=delta)
            if delta == 0:
                self.active = False
                self.render_error_start_time = None
                self.error_messages = self.error_messages[1:]


class AccountCreation(State):

    def __init__(self, name, state_machine, FPSCLOCK, DISPLAYSURF, server_host, server_port):
        State.__init__(self)
        self.name = name
        self.state_machine = state_machine
        self.FPSCLOCK = FPSCLOCK
        self.DISPLAYSURF = DISPLAYSURF
        self.resource_manager = ResourceManager()
        self.login_server_client = LoginServerClient(server_host, server_port)
        self.error_message_drawer = ErrorMessageDrawer(WINDOWHEIGHT/5)

        # Create the GUI Layer
        self.login_gui_layer = GUILayer(WINDOWWIDTH, WINDOWHEIGHT)

        # Add all the TextFields and Buttons
        name_field_rect = (WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 150, 200, 40)
        name_field = TextGUI('name', name_field_rect, initial_value='', shadow_value="Username")
        self.login_gui_layer.add(name_field)

        pw_gui_rect_1 = (WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 100, 200, 40)
        pw_gui_1 = PasswordTextGUI('password1', pw_gui_rect_1, initial_value='', shadow_value="Password")
        self.login_gui_layer.add(pw_gui_1)

        pw_gui_rect_2 = (WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 50, 200, 40)
        pw_gui_2 = PasswordTextGUI('password2', pw_gui_rect_2, initial_value='', shadow_value="Repeat")
        self.login_gui_layer.add(pw_gui_2)

        create_button_rect = (WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 +70, 200, 40)
        create_button = ButtonGUI('create', create_button_rect, "Create", function=self.create_character)
        self.login_gui_layer.add(create_button)

        back_button_rect = (WINDOWWIDTH / 2 - 100, (WINDOWHEIGHT / 2) + 120, 200, 50)
        back_button = ButtonGUI('back', back_button_rect, "Back", function=self.back_to_login)
        self.login_gui_layer.add(back_button)

        # Create the Focus Tab Chain and set the initial Focus
        name_field.focus = True
        self.login_gui_layer.add_tab_element('name')
        self.login_gui_layer.add_tab_element('password1')
        self.login_gui_layer.add_tab_element('password2')

    def update(self):
        # Get all the events that are there
        events = pygame.event.get()

        for event in events:
            if (event.type == KEYDOWN or event.type == KEYUP) and event.key == K_ESCAPE:
                exit(0)

        # Drawing the screen black
        self.DISPLAYSURF.fill(BGCOLOR)

        draw_text_on_screen_at(self.DISPLAYSURF, "Create Account", WINDOWWIDTH / 2, 70, 72)

        # Passing the renderer and the events to the gui handler for possible text inputs
        self.login_gui_layer.draw_gui(self.DISPLAYSURF, events)

        self.error_message_drawer.draw(self.DISPLAYSURF)

        # Update Screen and Clock
        pygame.display.update()
        self.FPSCLOCK.tick(FPS)

    def create_character(self):
        login = self.login_gui_layer.get_by_name('name').get_value()
        password1 = self.login_gui_layer.get_by_name('password1').get_value()
        password2 = self.login_gui_layer.get_by_name('password2').get_value()

        if password1 == password2 and password1 != "" and len(password1) > 5:
            #self.login_server_client.create_account(login, password1)
            account_creation = self.login_server_client.create_account(username=login, password=password1)

            assert account_creation is not None

            if account_creation.success:
                    self.state_machine.transition("character_selection",
                                                  {
                                                      "session_key": account_creation.session_key,
                                                      "account_id": account_creation.account_id,
                                                      "available_characters": account_creation.available_characters
                                                  })
            else:
                if account_creation.code == AccountResponse.DOUBLE_USERNAME:
                    self.login_gui_layer.get_by_name("name").set_invalid_entry(True)
                    self.error_message_drawer.add(account_creation.reason, 2)
                else:
                    print account_creation.code
        else:
            self.login_gui_layer.get_by_name('password1').set_invalid_entry(True)
            self.login_gui_layer.get_by_name('password2').set_invalid_entry(True)
            self.error_message_drawer.add("Passwords must match, non empty and longer than 5 characters!", 4)

    def back_to_login(self):
        self.state_machine.transition("login", {})

    def exit_state(self):
        self.login_gui_layer.get_by_name('password1').set_invalid_entry(False)
        self.login_gui_layer.get_by_name('password2').set_invalid_entry(False)
        self.login_gui_layer.get_by_name("name").set_invalid_entry(False)
        self.login_gui_layer.get_by_name('name').value = ""
        self.login_gui_layer.get_by_name('password1').value = ""
        self.login_gui_layer.get_by_name('password2').value = ""