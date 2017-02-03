# -*- coding:utf-8 -*-
import pygame
from client.config import WINDOWWIDTH, WINDOWHEIGHT
from client.drawers.BasicHealthModifierDrawer import BasicHealthModifierDrawer
from client.drawers.BasicLayoutDrawer import BasicLayoutDrawer
from client.gui_lib.ButtonGUI import ButtonGUI


class ExistingGUILayer():

    def __init__(self, client_level_manager, resource_manager, game_gui_layer, client_input_handler, looting_gui,
                 inventory_gui, description_gui, crafting_gui, npc_interaction_gui, state_machine):

         # First we create new surface with the same size as the window
        self.layer_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA, 32)
        self.layer_surface = self.layer_surface.convert_alpha()

        self.game_gui_layer = game_gui_layer
        self.layer_surface = self.layer_surface
        self.client_input_handler = client_input_handler

        self.looting_gui = looting_gui
        self.inventory_gui = inventory_gui
        self.description_gui = description_gui
        self.crafting_gui = crafting_gui
        self.npc_interaction_gui = npc_interaction_gui
        self.state_machine = state_machine
        self.basic_health_modifier_drawer = BasicHealthModifierDrawer(resource_manager)
        self.basic_layout_drawer = BasicLayoutDrawer(resource_manager)
        self.client_level_manager = client_level_manager

        self.graphics = resource_manager.load_image('layout/gui')

        self.craft = self.graphics.subsurface(pygame.Rect(0, 174, 61, 61))
        self.craft_hover = self.graphics.subsurface(pygame.Rect(62, 174, 61, 61))
        self.loot = self.graphics.subsurface(pygame.Rect(0, 236, 61, 61))
        self.loot_hover = self.graphics.subsurface(pygame.Rect(62, 236, 61, 61))
        self.backpack = self.graphics.subsurface(pygame.Rect(0, 298, 61, 61))
        self.backpack_hover = self.graphics.subsurface(pygame.Rect(62, 298, 61, 61))

        bg1 = ButtonGUI("backpack_button", pygame.Rect(WINDOWWIDTH-75+7, 0+7, 61, 61), "", lambda: None,
                        texture=self.backpack, texture_hover=self.backpack_hover)
        self.game_gui_layer.add(bg1)
        self.game_gui_layer.register_function_on('backpack_button', self.inventory_gui.back_pack_toggle_command)

        bg1 = ButtonGUI("craft_button", pygame.Rect(WINDOWWIDTH-75+7, 225+7, 61, 61), "", lambda: None,
                        texture=self.craft, texture_hover=self.craft_hover)
        self.game_gui_layer.add(bg1)
        self.game_gui_layer.register_function_on('craft_button', self.crafting_gui.crafting_toggle_command)

        bg1 = ButtonGUI("loot_button", pygame.Rect(WINDOWWIDTH-75+7, 450+7, 61, 61), "", lambda: None,
                        texture=self.loot, texture_hover=self.loot_hover)
        self.game_gui_layer.add(bg1)
        self.game_gui_layer.register_function_on('loot_button', self.looting_gui.looting_toggle_command)

        # Give the reference points to the container UIs
        # The reference point is the right-top-most point of the container such that it is aligned with the four buttons
        self.inventory_gui.set_reference_point(WINDOWWIDTH-90, 0)
        self.crafting_gui.set_reference_point(WINDOWWIDTH-90, 225)
        self.looting_gui.set_reference_point(WINDOWWIDTH-90, 450)

    def clear(self):
        self.layer_surface.fill((0, 0, 0, 0))

    def draw_layout_on_top_and_health_icons(self):

        # Get the current level
        current_level = self.client_level_manager.get_current_level()

        if current_level is None:
            return

        # First get the width and height of the level
        width, height = current_level.get_size()

        # Make sure we only draw things if we have a level boundary
        if height is None or width is None:
            return

        self.basic_layout_drawer.draw(self.layer_surface, current_level)
        self.basic_health_modifier_drawer.draw(self.layer_surface, current_level)

    def draw(self):

        self.clear()

        events = pygame.event.get()

        # Update gui if necessary
        if self.game_gui_layer.some_element_has_focus():
            self.game_gui_layer.draw_gui(self.layer_surface, events)
        else:
            self.game_gui_layer.draw_gui(self.layer_surface, [])
            # Now care about user input and send it to the server
            self.client_input_handler.execute(events)


        # First draw some underground things
        self.looting_gui.pre_draw_step(self.layer_surface)
        self.inventory_gui.pre_draw_step(self.layer_surface)
        self.crafting_gui.pre_draw_step(self.layer_surface)

        # Draw the three Item Handling GUIs
        self.looting_gui.execute(self.layer_surface)
        self.inventory_gui.execute(self.layer_surface)
        self.crafting_gui.execute(self.layer_surface)

        #Draw the Description GUI On Top if necessary
        self.description_gui.draw()

        self.npc_interaction_gui.draw(self.layer_surface)

        self.draw_layout_on_top_and_health_icons()


