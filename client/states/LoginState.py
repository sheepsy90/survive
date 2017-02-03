# -*- coding:utf-8 -*-
import pygame
from pygame.constants import KEYDOWN, KEYUP, K_ESCAPE
from client.colours import BGCOLOR, GREEN, DARKGREEN, RED, BLACK

from client.config import WINDOWHEIGHT, WINDOWWIDTH, FPS
from client.drawers.PhotoBackgroundSystem import PhotoBackgroundSystem
from client.drawers.helper import draw_text_on_screen_at
from client.gui_lib.ButtonGUI import ButtonGUI
from client.gui_lib.GUILayer import GUILayer
from client.gui_lib.PasswordTextGUI import PasswordTextGUI
from client.gui_lib.TextGUI import TextGUI
from client.network.LoginServiceClient import LoginServerClient, AccountResponse
from client.sound.ResourceManager import ResourceManager
from client.states.AccountCreation import ErrorMessageDrawer
from client.states.State import State


class LoginState(State):

    def __init__(self, name, state_machine, FPSCLOCK, DISPLAYSURF, server_host, server_port):
        State.__init__(self)
        self.name = name
        self.state_machine = state_machine
        self.FPSCLOCK = FPSCLOCK
        self.DISPLAYSURF = DISPLAYSURF
        self.resource_manager = ResourceManager()
        self.login_server_client = LoginServerClient(server_host, server_port)
        self.render_connection_error_flag = False
        self.render_connection_error_start_time = None
        self.error_message_drawer = ErrorMessageDrawer(WINDOWHEIGHT/2)

        self.photo_background_system = PhotoBackgroundSystem(resource_manager=self.resource_manager)

        # Create the GuiLayer and the UI Elements
        self.login_gui_layer = GUILayer(WINDOWWIDTH, WINDOWHEIGHT)
        self.create_ui_elements()

    def update(self):
        # Get all the events that are there
        events = pygame.event.get()

        for event in events:
            if (event.type == KEYDOWN or event.type == KEYUP) and event.key == K_ESCAPE:
                exit(0)

        # Drawing the screen black
        self.DISPLAYSURF.fill(BGCOLOR)

        self.photo_background_system.draw(self.DISPLAYSURF)

        draw_text_on_screen_at(self.DISPLAYSURF, "Arcology", WINDOWWIDTH / 2, 70, 120)
        draw_text_on_screen_at(self.DISPLAYSURF, "Mankinds leftovers", WINDOWWIDTH / 2, 170, 48)

        self.error_message_drawer.draw(self.DISPLAYSURF)

        # Passing the renderer and the events to the gui handler for possible text inputs
        self.login_gui_layer.draw_gui(self.DISPLAYSURF, events)

        # Update Screen and Clock
        pygame.display.update()
        self.FPSCLOCK.tick(FPS)

    def set_continue_to_account_selection(self):
        self.state_machine.transition("account_creation", {})

    def continue_to_character_selection(self):
        login_field = self.login_gui_layer.get_by_name('name')
        login = login_field.get_value()
        password_field = self.login_gui_layer.get_by_name('password')
        password = password_field.get_value()

        account_result = self.login_server_client.general_login(login, password)

        if account_result.success:
            self.state_machine.transition("character_selection",
                                          {
                                              "session_key": account_result.session_key,
                                              "account_id": account_result.account_id,
                                              "available_characters": account_result.available_characters
                                          })
        else:
            if account_result.code == AccountResponse.INCORRECT_CREDENTIALS:
                login_field.set_invalid_entry(True)
                password_field.set_invalid_entry(True)
                self.error_message_drawer.add(account_result.reason, 2)
            if account_result.code == AccountResponse.NETWORK_ERROR:
                self.error_message_drawer.add("Could not connect to login server", 2)

    def create_ui_elements(self):
        # Create the buttons and text elements
        login_text_rect = (WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 150, 200, 40)
        login_text_field = TextGUI('name', login_text_rect, initial_value='', shadow_value="Username")
        self.login_gui_layer.add(login_text_field)

        password_field_rect = (WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 100, 200, 40)
        password_field = PasswordTextGUI('password', password_field_rect, initial_value='', shadow_value="Password")
        self.login_gui_layer.add(password_field)

        login_button_rect = (WINDOWWIDTH / 2 - 100, (WINDOWHEIGHT / 2)+50, 200, 50)
        login_button = ButtonGUI('login', login_button_rect, "Login", function=self.continue_to_character_selection,
                                 bg_color=DARKGREEN, focus_color=GREEN)
        self.login_gui_layer.add(login_button)

        create_account_button_rect = (WINDOWWIDTH / 2 - 100, (WINDOWHEIGHT / 2) + 110, 200, 50)
        create_account_button = ButtonGUI('create', create_account_button_rect, "Create Account",
                                          function=self.set_continue_to_account_selection, bg_color=DARKGREEN,
                                          focus_color=GREEN)
        self.login_gui_layer.add(create_account_button)

        login_text_field.focus = True
        self.login_gui_layer.add_tab_element('name')
        self.login_gui_layer.add_tab_element('password')