# -*- coding:utf-8 -*-

from client.gui_lib.LabelGUI import LabelGUI
from client.gui_use.GuiDragDropService import SupportsDrag, SupportsDrop
from client.gui_use.MouseMemorizer import MouseMemorizer


class EquipmentGUI(SupportsDrag, SupportsDrop):

    def __init__(self, rootx, rooty, equipment_logic, main_gui, drag_drop_service):
        SupportsDrag.__init__(self)
        SupportsDrop.__init__(self)

        self.equipment_logic = equipment_logic

        self.root_x = rootx
        self.root_y = rooty

        self.drag_drop_service = drag_drop_service
        self.drag_drop_service.register_me_on_drop(self)

        self.gui_element_shape = [rootx, rooty, 200, 300]

        self.background_label_hover = LabelGUI("equipment_label_background",
                           self.gui_element_shape,
                           label="",
                           non_focus_color=(150, 150, 150),
                           texture=None,
                           background_anyway=True)

        self.mouse_mem = MouseMemorizer(self.background_label_hover)

        main_gui.add(self.background_label_hover)


    def draw(self, renderer):
        if self.equipment_logic.is_visible():
            self.background_label_hover.set_visible(True)
        else:
            self.background_label_hover.set_visible(False)

    def notify_accepted(self, item):
        print "Notify"

    def finish_drop(self, item):
        print "Dropped"
