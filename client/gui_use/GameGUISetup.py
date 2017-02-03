# -*- coding:utf-8 -*-

from client.config import WINDOWWIDTH, WINDOWHEIGHT
from client.gui_lib.ButtonGUI import ButtonGUI
from client.gui_lib.GUILayer import GUILayer
from client.gui_lib.LabelGUI import LabelGUI
from client.gui_lib.TextGUI import TextGUI
from client.gui_use.ContainerGUI import ContainerGUI, InventoryGUI, CraftingGUI
from client.gui_use.GuiDragDropService import GuiDragDropService
from client.gui_use.NpcInteractionGUI import NpcInteractionGUI


class DescriptionGUI(object):

    def __init__(self, game_gui_layer, description_manager):
        self.game_gui_layer = game_gui_layer
        self.description_manager = description_manager

        self.t1 = TextGUI('description_text_gui', (100, 100, 400, 50),
                     maxlength=70, initial_value="Describe what you just made", non_focus_color=(150, 150, 150))
        self.button = ButtonGUI('description_button_submit', (300, 150, 100, 25), caption="Submit", function=self.submit)

        self.game_gui_layer.add(self.t1)
        self.game_gui_layer.add(self.button)

    def draw(self):
        if self.description_manager.has_available_description_possibility():
            self.t1.set_visible(True)
            self.button.set_visible(True)
        else:
            self.t1.set_visible(False)
            self.button.set_visible(False)

    def submit(self):
        text = self.t1.get_value()
        self.description_manager.finish_description(text)

class GameGuiSetup():
    def __init__(self, resource_manager, client_socket_wrapper, sound_engine, looting_manager, backpack_manager,
                 crafting_manager, description_manager, wearing_manager, npc_system):

        # The things that are actually used here and not just for passing on
        self.resource_manager = resource_manager
        self.client_socket_wrapper = client_socket_wrapper
        self.sound_engine = sound_engine

        # The logical Containers for the items
        self.looting_manager = looting_manager
        self.backpack_manager = backpack_manager
        self.crafting_manager = crafting_manager
        self.wearing_manager = wearing_manager

        # Create the Drag Drop service some GUI Elements use to coordinate Drag'n Drop
        self.gui_drag_drop_service = GuiDragDropService()

        # Call the creators for the single gui elements
        self.game_gui_layer = self.create_game_gui_layer()

        self.inventory_gui = InventoryGUI(self.backpack_manager, self.game_gui_layer, self.gui_drag_drop_service,
                                          self.resource_manager, self.client_socket_wrapper, self.wearing_manager)

        self.inventory_gui.set_sound_engine(sound_engine)

        self.looting_manager_gui = ContainerGUI(self.looting_manager, self.game_gui_layer, self.gui_drag_drop_service,
                                                self.resource_manager, self.client_socket_wrapper)

        self.crafting_gui = CraftingGUI(self.crafting_manager, self.game_gui_layer, self.gui_drag_drop_service,
                                        self.resource_manager, self.client_socket_wrapper)

        self.description_gui = DescriptionGUI(self.game_gui_layer, description_manager)

        self.npc_interaction_gui = NpcInteractionGUI(self.game_gui_layer, self.resource_manager, npc_system)

    def create_game_gui_layer(self):
        return GUILayer(WINDOWWIDTH, WINDOWHEIGHT)

    def get_game_gui_layer(self):
        return self.game_gui_layer

    def get_crafting_gui(self):
        return self.crafting_gui

    def get_looting_gui(self):
        return self.looting_manager_gui

    def get_inventory_gui(self):
        return self.inventory_gui

    def get_description_gui(self):
        return self.description_gui

    def get_npc_interaction_gui(self):
        return self.npc_interaction_gui