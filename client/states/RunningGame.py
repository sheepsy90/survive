# -*- coding:utf-8 -*-
from Queue import Queue
import pygame
import socket
import threading
import time

from client.colours import BLACK
from client.config import WINDOWWIDTH, WINDOWHEIGHT, CELLSIZE, FPS
from client.drawers.BasicEffectDrawer import EffectList
from client.drawers.BasicMarkerDrawer import MarkerLogic
from client.drawers.GameStateDrawer import GameStateDrawer
from client.effects.CameraShake import CameraShaker
from client.gui_use.GameGUISetup import GameGuiSetup
from client.gui_use.WindowLayer import ExistingGUILayer
from client.input.ClientInputHandler import ClientInputHandler
from client.local_objects.ClientLevelManager import ClientLevelManager
from client.logic.DescriptionManager import DescriptionManager
from client.logic.LootingContainerManager import BackpackContainerManager, LootingContainerManager, \
    CraftingContainerManager
from client.logic.NpcSystem import NpcSystem
from client.logic.ServerCommandDispatcher import ServerCommandDispatcher
from client.logic.StateMachine import StateMachine
from client.logic.TutorialStateMachine import TutorialStateMachine
from client.network.ClientSocketWrapper import ClientSocketWrapper
from client.sound.ResourceManager import ResourceManager
from client.sound.VoiceActingEngine import VoiceActingEngine
from client.states.State import State
from common.constants.ClientPackagePrefixes import ClientPackagePrefixes
from common.helper import determine_package_length


class RunningGame(State, threading.Thread):

    def __init__(self, name, gstate_machine, FPSCLOCK, DISPLAYSURF,  sound_engine, music_engine):
        threading.Thread.__init__(self)
        self.daemon = True

        self.name = name
        self.gstate_machine = gstate_machine
        self.FPSCLOCK = FPSCLOCK
        self.DISPLAYSURF = DISPLAYSURF
        self.music_engine = music_engine
        self.sound_engine = sound_engine

        self.send_something_win32_flag = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.udp_ip = None
        self.udp_port = None
        self.state_machine = StateMachine()
        self.client_socket_wrapper = ClientSocketWrapper(self.sock, self.udp_ip, self.udp_port)
        self.input_queue = Queue()

        self.voice_engine = VoiceActingEngine(self.sound_engine)

        self.client_level_manager = ClientLevelManager(sound_engine)

        self.resource_manager = ResourceManager()

        # Create the logical objects which are necessary to store the items representations
        self.looting_container_manager = LootingContainerManager()
        self.backpack_container_manager = BackpackContainerManager()
        self.crafting_container_manager = CraftingContainerManager()

        self.description_manager = DescriptionManager(self.client_socket_wrapper)

        self.wearing_manager = self.client_level_manager.get_wearing_manager()

        self.npc_system = NpcSystem()
        self.effect_list = EffectList()

        # Create a Command Dispatcher to extract the update of the local level from this method/class
        self.server_command_dispatcher = ServerCommandDispatcher(self.state_machine,
                                                                self.client_level_manager,
                                                                self.sound_engine,
                                                                self.client_socket_wrapper,
                                                                self.looting_container_manager,
                                                                self.backpack_container_manager,
                                                                self.crafting_container_manager,
                                                                self.description_manager,
                                                                self.wearing_manager,
                                                                self.npc_system,
                                                                self.effect_list)

        # Create the Game GUI and give it teh necessary logical classes to work on
        ggs = GameGuiSetup(self.resource_manager,
                           self.client_socket_wrapper,
                           self.sound_engine,
                           self.looting_container_manager,
                           self.backpack_container_manager,
                           self.crafting_container_manager,
                           self.description_manager,
                           self.wearing_manager,
                           self.npc_system)

        # Get the GUI Elements that need to be called within the main game loop
        game_gui_layer = ggs.get_game_gui_layer()

        looting_gui = ggs.get_looting_gui()
        inventory_gui = ggs.get_inventory_gui()
        crafting_gui = ggs.get_crafting_gui()

        description_gui = ggs.get_description_gui()
        npc_interaction_gui = ggs.get_npc_interaction_gui()

        # Define the Input Handler for the Client which processes the input (keyboard/mouse)
        client_input_handler = ClientInputHandler(self.client_level_manager,
                                                  self.sound_engine,
                                                  self.client_socket_wrapper)

        self.marker_logic = MarkerLogic()

        tsm = TutorialStateMachine(self.voice_engine, self.sound_engine, self.client_level_manager, self.marker_logic)
        camera_shaker = CameraShaker()

        self.gui_layer = ExistingGUILayer(self.client_level_manager, self.resource_manager, game_gui_layer,
                                     client_input_handler, looting_gui, inventory_gui,
                                     description_gui, crafting_gui, npc_interaction_gui, self.state_machine)

        # The Drawer for the game window with all the objects and the player and so on
        self.gsd = GameStateDrawer(self.client_level_manager, self.resource_manager, self.marker_logic, tsm, camera_shaker,
                                   self.state_machine, self.effect_list)

        self.active = False

    def run(self):
        """ This method reads the information from the server and processes the packages """

        while self.active:
            if not self.send_something_win32_flag:
                continue

            data, addr = self.sock.recvfrom(1024)

            package_length = determine_package_length(data[0:2])
            package = data[2:package_length + 2]

            command = package[0:3]

            self.input_queue.put((command, package[3:]))

        print "Run Method terminates"

    def enter_state(self, property_dict):
        self.state_machine.set_account_id(property_dict["account_id"])
        self.state_machine.set_character_id(property_dict["char_id_chosen"])
        self.state_machine.set_session_key(property_dict["session_key"])

        ip, port = property_dict["connection_info"]
        self.client_socket_wrapper.set_new_connection_info(ip, port)

        self.state_machine.set_character_is_still_tutorial(property_dict["is_tutorial"])
        # Reset the mouse cursor if it has still a diamond from hover
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        self.active = True
        self.start()

    def exit_state(self):
        self.active = False

    def update(self):
        # If the game is not connected yet do so
        if self.state_machine.is_not_connected():
            session_key = self.state_machine.get_session_key()
            account_id = self.state_machine.get_account_id()
            character_id = self.state_machine.get_character_id()
            self.client_socket_wrapper.send_login_message_to_game_server(session_key, account_id, character_id)
            self.state_machine.set_connected(True)
            self.send_something_win32_flag = True
        else:
            # Send a TTL to the server each two seconds
            if time.time() > self.state_machine.last_time_ttl() + 2:
                self.client_socket_wrapper.send_message(ClientPackagePrefixes.CLIENT_SENDS_TTL)
                self.state_machine.refresh_last_time_ttl()

            if not self.input_queue.empty():
                self.state_machine.update_time_heard_from_server()

            if self.state_machine.is_last_time_heard_from_server_longer_than(4):
                self.gstate_machine.transition("login", {})

            # First care about all things that are there from the server
            while not self.input_queue.empty():
                command, info = self.input_queue.get()
                self.server_command_dispatcher.dispatch_server_instruction(command, info)

            # If there is a state which is not drawable we don't draw anything
            if not self.is_current_level_drawable():
                return

            # First of all fill the complete surface with red color so we can see the different parts later on
            self.DISPLAYSURF.fill(BLACK)

            # Draw the level state and place it onto the main display surface
            self.gsd.draw()

            # Our GUI Surface is 20x20 sow e want to determine the center
            x_off = (WINDOWWIDTH - CELLSIZE * 20) / 2
            y_off = (WINDOWHEIGHT - CELLSIZE * 20) / 4
            self.DISPLAYSURF.blit(self.gsd.layer_surface, pygame.Rect(x_off, y_off, WINDOWWIDTH, WINDOWHEIGHT))

            self.gui_layer.draw()
            self.DISPLAYSURF.blit(self.gui_layer.layer_surface, pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT))


            # self.sound_engine.play_or_keep_going("alert")
            #self.sound_engine.play_or_keep_going("arcology_ki")
            self.voice_engine.update(self.DISPLAYSURF)

            # Update and FPS timing
            pygame.display.flip()
            self.FPSCLOCK.tick(FPS)

    def is_current_level_drawable(self):
        # Check if the current level
        level = self.client_level_manager.get_current_level()
        if level is None or not level.get_player_manager().has_me():
            return False
        return True