# -*- coding:utf-8 -*-
import pygame
from pygame.constants import KEYDOWN, KEYUP, K_ESCAPE
from client.colours import WHITE, BLACK, BGCOLOR
from client.config import WINDOWHEIGHT, WINDOWWIDTH, FPS
from client.drawers.BasicLayoutDrawer import OwnSurface
from client.gui_lib.ButtonGUI import ButtonGUI
from client.gui_lib.GUILayer import GUILayer
from client.network.LoginServiceClient import LoginServerClient, CharacterPayload
from client.sound.ResourceManager import ResourceManager
from client.states.State import State


TEXT = """Character description dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
             dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
             ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
             fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
             mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
             tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
             ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
             voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
             proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""


class CharacterSelectionField():

    def __init__(self, character_selection_slot_id):
        self.character_selection_slot_id = character_selection_slot_id
        self.button = None
        self.char_id = None
        self.name = None
        self.description = "Dummy"

    def get_character_slot_id(self):
        return self.character_selection_slot_id

    def set_character_id(self, character_id):
        self.char_id = character_id

    def set_name(self, name):
        self.name = name

    def set_description(self, desc):
        self.description = desc

    def get_description(self):
        return self.description

    def get_char_id(self):
        return self.char_id

    def get_data(self):
        return [self.char_id, self.name]

    def set_button_which_belongs_to_that_field(self, btn):
        self.button = btn

    def update_button(self, click_pointer, existing_character, non_existing_character):

        if self.char_id is not None:
            self.button.function = lambda: click_pointer(self.character_selection_slot_id, self.char_id)
            self.button.texture = existing_character
            self.button.texture_hover = existing_character
        else:
            self.button.function = lambda: click_pointer(self.character_selection_slot_id, None)
            self.button.texture = non_existing_character
            self.button.texture_hover = non_existing_character


class CharacterSelection(State):

    def __init__(self, name, state_machine, FPSCLOCK, DISPLAYSURF, server_host, server_port):
        State.__init__(self)
        self.name = name
        self.state_machine = state_machine
        self.FPSCLOCK = FPSCLOCK
        self.DISPLAYSURF = DISPLAYSURF
        self.resource_manager = ResourceManager()
        self.login_server_client = LoginServerClient(server_host, server_port)
        self.titleFont = pygame.font.Font('freesansbold.ttf', 16)

        self.character_slots = {
            e.get_character_slot_id(): e for e in [CharacterSelectionField(1),
                                                   CharacterSelectionField(2),
                                                   CharacterSelectionField(3),
                                                   CharacterSelectionField(4)]
        }

        self.layout_graphic = self.resource_manager.load_image('layout/gui')

        self.vertical_border = OwnSurface(self.layout_graphic.subsurface(pygame.Rect(164, 304, 8, 8)))
        self.horizontal_border = OwnSurface(self.layout_graphic.subsurface(pygame.Rect(182, 313, 8, 8)))
        self.corner_left_bottom = OwnSurface(self.layout_graphic.subsurface(pygame.Rect(164, 313, 8, 8)))
        self.corner_right_bottom = OwnSurface(self.layout_graphic.subsurface(pygame.Rect(173, 313, 8, 8)))
        self.corner_right_top = OwnSurface(self.layout_graphic.subsurface(pygame.Rect(173, 304, 8, 8)))

        self.character_layout_graphics = OwnSurface(self.layout_graphic.subsurface(pygame.Rect(164, 154, 112, 149)))
        self.existing_character = self.layout_graphic.subsurface(pygame.Rect(277, 154, 98, 98))
        self.no_character = self.layout_graphic.subsurface(pygame.Rect(277, 253, 98, 98))

        self.login_gui_layer = GUILayer(WINDOWWIDTH, WINDOWHEIGHT)

        self.pos_surfaces = [
            (0+7, 0+7, 98, 98),
            (WINDOWWIDTH/2+7, 0+7, 98, 98),
            (0+7, WINDOWHEIGHT/2+7, 98, 98),
            (WINDOWWIDTH/2+7, WINDOWHEIGHT/2+7, 98, 98)
        ]

        self.pos = [
            (0, 0, 98, 98),
            (WINDOWWIDTH/2, 0, 98, 98),
            (0, WINDOWHEIGHT/2, 98, 98),
            (WINDOWWIDTH/2, WINDOWHEIGHT/2, 98, 98)
        ]

        button_1 = self.add_and_return_char_selection_button(1, self.pos_surfaces[0], self.choose_character_or_slot)
        button_2 = self.add_and_return_char_selection_button(2, self.pos_surfaces[1], self.choose_character_or_slot)
        button_3 = self.add_and_return_char_selection_button(3, self.pos_surfaces[2], self.choose_character_or_slot)
        button_4 = self.add_and_return_char_selection_button(4, self.pos_surfaces[3], self.choose_character_or_slot)

        self.character_slots[1].set_button_which_belongs_to_that_field(button_1)
        self.character_slots[2].set_button_which_belongs_to_that_field(button_2)
        self.character_slots[3].set_button_which_belongs_to_that_field(button_3)
        self.character_slots[4].set_button_which_belongs_to_that_field(button_4)

    def enter_state(self, dict_args):
        assert "session_key" in dict_args
        assert "account_id" in dict_args
        assert "available_characters" in dict_args


        self.session_key = dict_args["session_key"]
        self.account_id = dict_args["account_id"]

        self.switch_to_running = False
        self.switch_to_running_params = None
        self.switch_to_running_started = 0

        available_characters = dict_args["available_characters"]
        available_characters = [CharacterPayload.from_dict(e) for e in available_characters]

        # First we fill up the
        while len(available_characters) < 4:
            available_characters.append(CharacterPayload(None, "Name", "Dummy Descript"))

        # Then we update the slot info
        for i in range(len(available_characters)):
            char_selection_field = self.character_slots[i+1]
            char_selection_field.set_character_id(available_characters[i].character_id)
            char_selection_field.set_name(available_characters[i].name)
            char_selection_field.set_description(available_characters[i].description)
            char_selection_field.update_button(self.choose_character_or_slot, self.existing_character, self.no_character)



    def choose_character_or_slot(self, slot, char_id_chosen):
        print "User clicked on Slot", slot, "with char id", char_id_chosen

        session_key = self.session_key
        account_id = self.account_id

        if char_id_chosen is None:
            character_response = self.login_server_client.create_character(account_id, session_key)
            if character_response.success:
                single_char_payload = CharacterPayload.from_dict(character_response.character_payload)
                char_id = single_char_payload.character_id
                name = single_char_payload.name
                description = single_char_payload.description
                is_tutorial = character_response.is_still_tutorial
                self.add_new_character_locally(slot, char_id, name, description)
            else:
                raise Exception(character_response.reason)
        else:
            character_response = self.login_server_client.login_character(account_id, session_key, char_id_chosen)
            if character_response.success:
                connection_info = character_response.connection_info
                is_tutorial = character_response.is_still_tutorial
                switch_to_running_params = {
                    "session_key": self.session_key,
                    "account_id": self.account_id,
                    "is_tutorial": is_tutorial,
                    "char_id_chosen": char_id_chosen,
                    "connection_info": connection_info
                }
                self.state_machine.transition("running_game", switch_to_running_params)
            else:
                raise Exception(character_response.reason)

    def add_new_character_locally(self, slot, char_id_chosen, name, description):
        char_selection_field = self.character_slots[slot]
        char_selection_field.set_character_id(char_id_chosen)
        char_selection_field.set_name(name)
        char_selection_field.set_description(description)
        char_selection_field.update_button(self.choose_character_or_slot, self.existing_character, self.no_character)

    def add_and_return_char_selection_button(self, nr, rect, fkt_pointer):
        btn = ButtonGUI('char_{}'.format(nr),
                        rect,
                        "",
                        function=lambda: fkt_pointer(nr, None),
                        texture=self.no_character,
                        texture_hover=self.no_character)
        self.login_gui_layer.add(btn)
        return btn

    # Get all the events that are there
    def offset(self, character_layout_graphics, corner_left_bottom, corner_right_bottom, corner_right_top, horizontal_border,
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


    def drawText(self, surface, text, color, rect, font, aa=True, bkg=None):

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


    def draw_character_description(self, slot, character_layout_graphics, renderer, titleFont, text, x=0, y=0):
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
            self.drawText(text_sf, text,
                          BLACK, (0, 0, w, h), titleFont, aa=True, bkg=None)
            renderer.blit(text_sf, (16+x, character_layout_graphics.rect.height + 8+y, 1, 1))


    # TODO Wrapper this accordingly
    def shadow_out_no_chars(self, slot, renderer, x=0, y=0):
        if slot is None:
            c = (0, 0, 0, 150)
            s = pygame.Surface((WINDOWWIDTH / 2, WINDOWHEIGHT / 2), pygame.SRCALPHA, 32)
            s = s.convert_alpha()
            pygame.draw.rect(s, c, pygame.Rect(0, 0, WINDOWWIDTH / 2, WINDOWHEIGHT / 2))
            renderer.blit(s, pygame.Rect(x, y, WINDOWWIDTH / 2, WINDOWHEIGHT / 2))


    def write_char_name(self, slot, renderer, x=0, y=0):
        if slot[0] is not None:
            titleFont = pygame.font.Font('freesansbold.ttf', 16)
            g = titleFont.render(slot[1], True, BLACK)
            renderer.blit(g, pygame.Rect(x+12, y+120, 1, 1))


    def update(self):
        """ This method shows the login screen where the player can enter his credentials to authenticate at a login server and gets the initial server
            as well as his session key """


        events = pygame.event.get()

        for event in events:
            if (event.type == KEYDOWN or event.type == KEYUP) and event.key == K_ESCAPE:
                exit(0)

        # Drawing the screen black
        self.DISPLAYSURF.fill(BGCOLOR)

        pygame.draw.rect(self.DISPLAYSURF, WHITE, pygame.Rect(8, 8, WINDOWWIDTH/2-18, WINDOWHEIGHT/2-16))
        pygame.draw.rect(self.DISPLAYSURF, WHITE, pygame.Rect(8+WINDOWWIDTH/2, 8, WINDOWWIDTH/2-18, WINDOWHEIGHT/2-16))
        pygame.draw.rect(self.DISPLAYSURF, WHITE, pygame.Rect(8, WINDOWHEIGHT/2+8, WINDOWWIDTH/2-18, WINDOWHEIGHT/2-16))
        pygame.draw.rect(self.DISPLAYSURF, WHITE, pygame.Rect(8+WINDOWWIDTH/2, WINDOWHEIGHT/2+8, WINDOWWIDTH/2-18, WINDOWHEIGHT/2-16))

        self.draw_character_description(self.character_slots[1].get_char_id(), self.character_layout_graphics, self.DISPLAYSURF, self.titleFont, self.character_slots[1].get_description())
        self.draw_character_description(self.character_slots[2].get_char_id(), self.character_layout_graphics, self.DISPLAYSURF, self.titleFont, self.character_slots[2].get_description(), x=WINDOWWIDTH/2)
        self.draw_character_description(self.character_slots[3].get_char_id(), self.character_layout_graphics, self.DISPLAYSURF, self.titleFont, self.character_slots[3].get_description(), y=WINDOWHEIGHT/2)
        self.draw_character_description(self.character_slots[4].get_char_id(), self.character_layout_graphics, self.DISPLAYSURF, self.titleFont, self.character_slots[4].get_description(), x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2)

        # Draw the Gui Elements that are pressable
        self.login_gui_layer.draw_gui(self.DISPLAYSURF, events)

        # Overdraw that stuff with UI
        self.character_layout_graphics.draw_at(self.DISPLAYSURF, self.pos[0][0], self.pos[0][1])
        self.character_layout_graphics.draw_at(self.DISPLAYSURF, self.pos[1][0], self.pos[1][1])
        self.character_layout_graphics.draw_at(self.DISPLAYSURF, self.pos[2][0], self.pos[2][1])
        self.character_layout_graphics.draw_at(self.DISPLAYSURF, self.pos[3][0], self.pos[3][1])

        self.offset(self.character_layout_graphics, self.corner_left_bottom, self.corner_right_bottom, self.corner_right_top,
                    self.horizontal_border, self.DISPLAYSURF, self.vertical_border)

        self.offset(self.character_layout_graphics, self.corner_left_bottom, self.corner_right_bottom, self.corner_right_top,
                    self.horizontal_border, self.DISPLAYSURF, self.vertical_border, x=WINDOWWIDTH/2)

        self.offset(self.character_layout_graphics, self.corner_left_bottom, self.corner_right_bottom, self.corner_right_top,
                    self.horizontal_border, self.DISPLAYSURF, self.vertical_border, y=WINDOWHEIGHT/2)

        self.offset(self.character_layout_graphics, self.corner_left_bottom, self.corner_right_bottom, self.corner_right_top,
                    self.horizontal_border, self.DISPLAYSURF, self.vertical_border, x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2)

        self.shadow_out_no_chars(self.character_slots[1].get_char_id(), self.DISPLAYSURF)
        self.shadow_out_no_chars(self.character_slots[2].get_char_id(), self.DISPLAYSURF, x=WINDOWWIDTH/2)
        self.shadow_out_no_chars(self.character_slots[3].get_char_id(), self.DISPLAYSURF, y=WINDOWHEIGHT/2)
        self.shadow_out_no_chars(self.character_slots[4].get_char_id(), self.DISPLAYSURF, x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2)

        self.write_char_name(self.character_slots[1].get_data(), self.DISPLAYSURF)
        self.write_char_name(self.character_slots[2].get_data(), self.DISPLAYSURF, x=WINDOWWIDTH/2)
        self.write_char_name(self.character_slots[3].get_data(), self.DISPLAYSURF, y=WINDOWHEIGHT/2)
        self.write_char_name(self.character_slots[4].get_data(), self.DISPLAYSURF, x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2)

        # Update Screen and Clock
        pygame.display.update()
        self.FPSCLOCK.tick(FPS)