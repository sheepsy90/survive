# -*- coding:utf-8 -*-
import pygame

from pygame.constants import KEYDOWN, KEYUP, K_ESCAPE
from client.colours import BGCOLOR, WHITE, BLACK
from client.config import WINDOWWIDTH, WINDOWHEIGHT, FPS
from client.drawers.BasicLayoutDrawer import OwnSurface
from client.gui_lib.ButtonGUI import ButtonGUI
from client.gui_lib.GUILayer import GUILayer

TEXT = """Character description dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
             dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
             ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
             fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
             mollit anim id est laborum.  	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
             tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
             ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
             voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
             proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""


def draw_character_button(nr, rect, fkt_pointer, slots, login_gui_layer, existing_character, no_character):
    print slots
    if slots is None:
        login_gui_layer.add(ButtonGUI('char_%i' % nr, rect, "", function=lambda: fkt_pointer(None),
                                      texture=no_character, texture_hover=no_character))
    else:
        login_gui_layer.add(ButtonGUI('char_%i' % nr, rect, "", function=lambda: fkt_pointer(slots),
                                      texture=existing_character, texture_hover=existing_character))


# Get all the events that are there
def offset(character_layout_graphics, corner_left_bottom, corner_right_bottom, corner_right_top, horizontal_border,
           renderer, vertical_border, x=0, y=0):
    start_height = character_layout_graphics.rect.height
    start_width = character_layout_graphics.rect.width
    i = 0
    for i in range(start_height, (WINDOWHEIGHT / 2) - 16, 8):
        vertical_border.draw_at(renderer, 0+x, i+y)
    i += 8
    corner_left_bottom.draw_at(renderer, 0+x, i+y)
    j = 0
    for j in range(8, (WINDOWWIDTH / 2) - 16, 8):
        horizontal_border.draw_at(renderer, j+x, i+y)
    j += 8
    corner_right_bottom.draw_at(renderer, j+x, i+y)
    i -= 16
    for i in range((WINDOWHEIGHT / 2) - 19, 8, -8):
        vertical_border.draw_at(renderer, j+x, i+y)
    i -= 5
    vertical_border.draw_at(renderer, j+x, i+y)
    k = 0
    for k in range(start_width, (WINDOWWIDTH / 2) - 16, 8):
        horizontal_border.draw_at(renderer, k+x, 0+y)
    k += 8
    corner_right_top.draw_at(renderer, k+x, 0+y)


def drawText(surface, text, color, rect, font, aa=True, bkg=None):

    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


def draw_character_description(slot, character_layout_graphics, renderer, titleFont, text, x=0, y=0):
    w = WINDOWWIDTH / 2 - 40
    h = WINDOWHEIGHT / 2 - character_layout_graphics.rect.height - 32
    text_sf = pygame.Surface((w, h))
    text_sf.fill(WHITE)

    if slot == None:
        titleFont = pygame.font.Font('freesansbold.ttf', 64)
        g = titleFont.render("Free slot", True, BLACK)
        g = pygame.transform.rotate(g, 10.0)
        renderer.blit(g, (16+x, character_layout_graphics.rect.height+y, 1, 1))
    else:
        drawText(text_sf, text,
                 BLACK, (0, 0, w, h), titleFont, aa=True, bkg=None)
        renderer.blit(text_sf, (16+x, character_layout_graphics.rect.height + 8+y, 1, 1))


# TODO Wrapper this accordingly
def shadow_out_no_chars(slot, renderer, x=0, y=0):
    if slot is None:
        c = (0, 0, 0, 150)
        s = pygame.Surface((WINDOWWIDTH / 2, WINDOWHEIGHT / 2), pygame.SRCALPHA, 32)
        s = s.convert_alpha()
        pygame.draw.rect(s, c, pygame.Rect(0, 0, WINDOWWIDTH / 2, WINDOWHEIGHT / 2))
        renderer.blit(s, pygame.Rect(x, y, WINDOWWIDTH / 2, WINDOWHEIGHT / 2))


def write_char_name(slot, renderer, x=0, y=0):
    if slot[0] is not None:
        titleFont = pygame.font.Font('freesansbold.ttf', 16)
        g = titleFont.render(slot[1], True, BLACK)
        renderer.blit(g, pygame.Rect(x+12, y+120, 1, 1))


def show_character_selection(main_client, available_characters, resource_manager, fkt_pointer, renderer, FPSCLOCK):
        """ This method shows the login screen where the player can enter his credentials to authenticate at a login server and gets the initial server
            as well as his session key """
        login_gui_layer = GUILayer(WINDOWWIDTH, WINDOWHEIGHT)

        slots = available_characters

        pos_surfaces = [
            (0+7, 0+7, 98, 98),
            (WINDOWWIDTH/2+7, 0+7, 98, 98),
            (0+7, WINDOWHEIGHT/2+7, 98, 98),
            (WINDOWWIDTH/2+7, WINDOWHEIGHT/2+7, 98, 98)
        ]

        pos = [
            (0, 0, 98, 98),
            (WINDOWWIDTH/2, 0, 98, 98),
            (0, WINDOWHEIGHT/2, 98, 98),
            (WINDOWWIDTH/2, WINDOWHEIGHT/2, 98, 98)
        ]


        for i in range(4-len(available_characters)):
            slots.append([None, "Free character slot"])

        graphics = resource_manager.load_image('layout/gui')

        # The Elements for the left side of the screen
        character_layout_graphics = OwnSurface(graphics.subsurface(pygame.Rect(164, 154, 112, 149)))
        existing_character = graphics.subsurface(pygame.Rect(277, 154, 98, 98))
        no_character = graphics.subsurface(pygame.Rect(277, 253, 98, 98))

        vertical_border = OwnSurface(graphics.subsurface(pygame.Rect(164, 304, 8, 8)))
        horizontal_border = OwnSurface(graphics.subsurface(pygame.Rect(182, 313, 8, 8)))
        corner_left_bottom = OwnSurface(graphics.subsurface(pygame.Rect(164, 313, 8, 8)))
        corner_right_bottom = OwnSurface(graphics.subsurface(pygame.Rect(173, 313, 8, 8)))
        corner_right_top = OwnSurface(graphics.subsurface(pygame.Rect(173, 304, 8, 8)))

        draw_character_button(0, pos_surfaces[0], fkt_pointer, slots[0][0], login_gui_layer, existing_character, no_character)
        draw_character_button(1, pos_surfaces[1], fkt_pointer, slots[1][0], login_gui_layer, existing_character, no_character)
        draw_character_button(2, pos_surfaces[2], fkt_pointer, slots[2][0], login_gui_layer, existing_character, no_character)
        draw_character_button(3, pos_surfaces[3], fkt_pointer, slots[3][0], login_gui_layer, existing_character, no_character)

        titleFont = pygame.font.Font('freesansbold.ttf', 16)


        while not main_client.continue_to_game:

            events = pygame.event.get()

            for event in events:
                if (event.type == KEYDOWN or event.type == KEYUP) and event.key == K_ESCAPE:
                    exit(0)

            # Drawing the screen black
            renderer.fill(BGCOLOR)

            pygame.draw.rect(renderer, WHITE, pygame.Rect(8, 8, WINDOWWIDTH/2-18, WINDOWHEIGHT/2-16))
            pygame.draw.rect(renderer, WHITE, pygame.Rect(8+WINDOWWIDTH/2, 8, WINDOWWIDTH/2-18, WINDOWHEIGHT/2-16))
            pygame.draw.rect(renderer, WHITE, pygame.Rect(8, WINDOWHEIGHT/2+8, WINDOWWIDTH/2-18, WINDOWHEIGHT/2-16))
            pygame.draw.rect(renderer, WHITE, pygame.Rect(8+WINDOWWIDTH/2, WINDOWHEIGHT/2+8, WINDOWWIDTH/2-18, WINDOWHEIGHT/2-16))

            draw_character_description(slots[0][0], character_layout_graphics, renderer, titleFont, TEXT)
            draw_character_description(slots[1][0], character_layout_graphics, renderer, titleFont, TEXT, x=WINDOWWIDTH/2)
            draw_character_description(slots[2][0], character_layout_graphics, renderer, titleFont, TEXT, y=WINDOWHEIGHT/2)
            draw_character_description(slots[3][0], character_layout_graphics, renderer, titleFont, TEXT, x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2)

            # Draw the Gui Elements that are pressable
            login_gui_layer.draw_gui(renderer, events)

            # Overdraw that stuff with UI
            character_layout_graphics.draw_at(renderer, pos[0][0], pos[0][1])
            character_layout_graphics.draw_at(renderer, pos[1][0], pos[1][1])
            character_layout_graphics.draw_at(renderer, pos[2][0], pos[2][1])
            character_layout_graphics.draw_at(renderer, pos[3][0], pos[3][1])

            offset(character_layout_graphics, corner_left_bottom, corner_right_bottom, corner_right_top,
                   horizontal_border, renderer, vertical_border)

            offset(character_layout_graphics, corner_left_bottom, corner_right_bottom, corner_right_top,
                   horizontal_border, renderer, vertical_border, x=WINDOWWIDTH/2)

            offset(character_layout_graphics, corner_left_bottom, corner_right_bottom, corner_right_top,
                   horizontal_border, renderer, vertical_border, y=WINDOWHEIGHT/2)

            offset(character_layout_graphics, corner_left_bottom, corner_right_bottom, corner_right_top,
                   horizontal_border, renderer, vertical_border, x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2)

            shadow_out_no_chars(slots[0][0], renderer)
            shadow_out_no_chars(slots[1][0], renderer, x=WINDOWWIDTH/2)
            shadow_out_no_chars(slots[2][0], renderer, y=WINDOWHEIGHT/2)
            shadow_out_no_chars(slots[3][0], renderer, x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2)

            write_char_name(slots[0], renderer)
            write_char_name(slots[1], renderer, x=WINDOWWIDTH/2)
            write_char_name(slots[2], renderer, y=WINDOWHEIGHT/2)
            write_char_name(slots[3], renderer, x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2)


            # Update Screen and Clock
            pygame.display.update()
            FPSCLOCK.tick(FPS)