import pygame
from client.colours import WHITE, BLACK
from client.gui_lib.GUIElement import GUIElement


class LabelGUI(GUIElement):

    def __init__(self, name, rect, label, texture=None, non_focus_color=WHITE, background_anyway=False):
        GUIElement.__init__(self, name, rect)
        self.label = label
        self.texture = texture
        self.non_focus_color = non_focus_color
        self.background_anyway = background_anyway

    def draw(self, renderer):
        rect = self.get_rect()

        if self.texture is not None:
            if self.background_anyway:
                pygame.draw.rect(renderer, self.non_focus_color, self.get_rect())

            surface = pygame.transform.scale(self.texture, (rect.width, rect.height))
            renderer.blit(surface, rect)
        else:
            pygame.draw.rect(renderer, self.non_focus_color, self.get_rect())
        rendered_text = self.titleFont.render(self.label, True, BLACK)
        surface = pygame.transform.scale(rendered_text, (self.width, self.height))
        renderer.blit(surface, self.get_rect())
