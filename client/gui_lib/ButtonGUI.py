import pygame
import time

from client.gui_lib.GUIElement import GUIElement


class ButtonGUI(GUIElement):

    def __init__(self, name, rect, caption, function, text_rect=None, fg_color=(0, 0, 0), bg_color=(255, 255, 255), focus_color=(100, 100, 100), texture=None, texture_hover=None, bg_anyway=False):
        GUIElement.__init__(self, name, rect)
        self.function = function
        self.caption = caption
        self.texture = texture
        self.texture_hover = texture_hover
        self.fg_color = fg_color
        self.text_rect = text_rect
        self.bg_color = bg_color
        self.bg_anyway = bg_anyway
        self.focus_color = focus_color
        self.mouse_state = 0
        self.mouse_state_time = None

    def draw(self, renderer):

        rect = self.get_rect()

        if self.texture is not None:
            if not self.is_hover_active():
                if self.bg_anyway:
                    pygame.draw.rect(renderer, self.bg_color, self.get_rect())
                surface = pygame.transform.scale(self.texture, (rect.width, rect.height))
                renderer.blit(surface, rect)
            else:
                if self.bg_anyway:
                    pygame.draw.rect(renderer, self.bg_color, self.get_rect())
                surface = pygame.transform.scale(self.texture_hover, (rect.width, rect.height))
                renderer.blit(surface, rect)
        else:
            if self.is_hover_active():
                pygame.draw.rect(renderer, self.focus_color, self.get_rect())
            else:
                pygame.draw.rect(renderer, self.bg_color, self.get_rect())

        rendered_text = self.titleFont.render(self.caption, True, self.fg_color)

        if self.text_rect is not None:
            rect = pygame.Rect(self.text_rect)
            surface = pygame.transform.scale(rendered_text, (rect.width, rect.height))
            renderer.blit(surface, rect)
        else:
            surface = pygame.transform.scale(rendered_text, (self.width, self.height))
            renderer.blit(surface, self.get_rect())

    def update(self, mx, my, mouse_buttons, events):
        GUIElement.update(self, mx, my, mouse_buttons, events)

        mb1 = mouse_buttons[0]

        # TODO - Beautify soon !!!
        # Dummy way of click recognition - use events rather than that stupid thing
        if self.is_hover_active() and mb1 == 1 and self.mouse_state == 0:
            self.mouse_state = 1
            self.mouse_state_time = time.time()

        elif self.is_hover_active() and mb1 == 0 and self.mouse_state == 1:
            if time.time() - self.mouse_state_time < 0.3:
                self.mouse_state = 2
            else:
                self.mouse_state = 0
                self.mouse_state_time = None

        elif self.mouse_state == 2:
            self.handle_click()
            self.mouse_state = 0
            self.mouse_state_time = None

    def handle_click(self):
        if self.function is not None:
            self.function()
