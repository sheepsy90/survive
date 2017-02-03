import pygame
from pygame.constants import KEYDOWN


class GUILayer(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.gui_elements = {}
        self.tab_elements = []

    def some_element_has_focus(self):
        return len([1 for e in self.gui_elements.values() if e.has_focus()])

    def get_element_focus(self):
        l = [e for e in self.gui_elements.values() if e.has_focus()]
        if len(l) == 1:
            return l[0]

    def get_by_name(self, name):
        assert name in self.gui_elements.keys()
        return self.gui_elements[name]

    def add(self, element):
        element.register_gui_handler(self)
        self.gui_elements[element.get_name()] = element

    def update(self, mouse_position, mouse_buttons, events):
        xm, ym = mouse_position

        tab_pressed = len([e for e in events if e.type == KEYDOWN and e.key == 9]) > 0
        if tab_pressed:
            e = self.get_element_focus()
            if e is not None and e.name in self.tab_elements:
                idx = self.tab_elements.index(e.name)
                idx += 1
                idx %= len(self.tab_elements)
                name_next_focus = self.tab_elements[idx]
                n = self.get_by_name(name_next_focus)
                e.focus = False
                n.focus = True


        for element in self.gui_elements.values():
            element.update(xm, ym, mouse_buttons, events)

    def notify_focus_gain(self, elem):
        for element in self.gui_elements.values():
            if element != elem:
                element.disable_focus()

    def register_function_on(self, name, fkt):
        assert name in self.gui_elements
        self.gui_elements[name].function = fkt

    def add_tab_element(self, gui_element_name):
        self.tab_elements.append(gui_element_name)

    def draw_gui(self, renderer, events):
        # Get the mouse position and so on
        mouse_position = pygame.mouse.get_pos()
        m1, m2, m3 = pygame.mouse.get_pressed()
        mouse_buttons = m1, m2, m3

        # First use the mouse position to set the hover states of all elements
        self.update(mouse_position, mouse_buttons, events)

        # Some general facts like if we need to change the mouse button
        at_least_one_hover = False

        elements = self.gui_elements.values()
        elements = sorted(elements, key=lambda e: e.get_zorder())

        for element in elements:
            if not element.is_visible():
                continue
            if element.is_hover_active():
                at_least_one_hover = True
            element.draw(renderer)

        # Check if we need to change the mouse button type
        if at_least_one_hover:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)