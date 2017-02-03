import pygame


class GUIElement(object):

    TEXT = 2
    BUTTON = 1

    def __init__(self, name, rect):
        self.name = name
        self.x, self.y, self.width, self.height = rect
        self.is_hover = False
        self.gui_handler = None
        self.focus = False
        self.visible = True
        self.z_order = 0
        self.titleFont = pygame.font.Font('resources/fonts/VENUSRIS.ttf', 64)

    def set_zorder(self, order):
        self.z_order = order

    def get_zorder(self):
        return self.z_order

    def get_name(self):
        return self.name

    def set_hover_state(self, mx, my):
        if self.x <= mx <= self.width+self.x and self.y <= my <= self.height+self.y:
            self.is_hover = True
        else:
            self.is_hover = False

    def update(self, mx, my, mouse_buttons, events):
        self.set_hover_state(mx, my)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_hover_active(self):
        return self.is_hover

    def draw(self, renderer):
        raise NotImplementedError

    def register_gui_handler(self, gui_handler):
        self.gui_handler = gui_handler

    def enable_focus(self):
        self.focus = True

    def disable_focus(self):
        self.focus = False

    def has_focus(self):
        return self.focus

    def set_visible(self, value):
        self.visible = value

    def is_visible(self):
        return self.visible