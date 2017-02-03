# -*- coding:utf-8 -*-

import pygame
from pygame.rect import Rect
from client.colours import RED, GREEN, WHITE, BLACK
from client.config import WINDOWWIDTH
from client.drawers.helper import draw_item_grid
from client.gui_lib.ButtonGUI import ButtonGUI
from client.gui_lib.LabelGUI import LabelGUI
from client.gui_use.GuiDragDropService import ItemDrag, SupportsDrop, SupportsDrag
from client.gui_use.ItemResourceMapper import ItemResourceMapper
from client.gui_use.MouseMemorizer import MouseMemorizer


class AbstractContainerGUI(SupportsDrag, SupportsDrop):

    ITEM_CELL_SIZE = 25
    BORDER = 4
    CLOSED = 1
    OPENED = 2

    def __init__(self, rootx, rooty, container_logic, main_gui, drag_drop_service, resource_manager, client_socket_wrapper, wearing_manager=None):
        SupportsDrag.__init__(self)
        SupportsDrop.__init__(self)

        self.root_x = rootx
        self.root_y = rooty

        self.container_logic = container_logic
        self.main_gui = main_gui
        self.drag_drop_service = drag_drop_service
        self.drag_drop_service.register_me_on_drop(self)
        self.client_socket_wrapper = client_socket_wrapper
        self.wearing_manager = wearing_manager

        self.item_resource_mapper = ItemResourceMapper(resource_manager)

        self.wearing_surface_slot_mapping = {
            "mask": resource_manager.load_image("wearing_graphics/mask"),
            "hand": resource_manager.load_image("wearing_graphics/hand"),
            "default": resource_manager.load_image("wearing_graphics/default")
        }

        # Initialize and calculate the GUI Shape
        self.gui_element_shape = [rootx, rooty, 0, 0]
        self.reference_point = (0, 0)

        self.background_label_hover = LabelGUI("background_label_%s" % self.container_logic.get_name(),
                           self.gui_element_shape,
                           label="",
                           non_focus_color=(0, 0, 0, 0),
                           texture=None)
        main_gui.add(self.background_label_hover)

        self.mouse_mem = MouseMemorizer(self.background_label_hover)

        self.update_gui_elements((0, 0))

        # Initial States
        self.gui_state = AbstractContainerGUI.CLOSED
        self.set_all_gui_element_visible_to(False)

    def toggle_visible_state_based_on_container_logic(self):
        if self.container_logic.is_container_open() and self.gui_state == ContainerGUI.CLOSED:
            self.gui_state = ContainerGUI.OPENED
            self.set_all_gui_element_visible_to(True)

        if not self.container_logic.is_container_open() and self.gui_state == ContainerGUI.OPENED:
            self.gui_state = ContainerGUI.CLOSED
            self.set_all_gui_element_visible_to(False)

    def set_all_gui_element_visible_to(self, state):
        self.background_label_hover.set_visible(state)

    def send_close_command(self):
        raise NotImplementedError

    def set_reference_point(self, x, y):
        self.reference_point = (x, y)

    def pre_draw_step(self, renderer):
        self.toggle_visible_state_based_on_container_logic()

        if self.gui_state == AbstractContainerGUI.OPENED:

            # First check if we can draw anything due to the validity of the logic container
            if not self.container_logic.is_valid():
                return

            shape = self.container_logic.get_shape()

            self.update_gui_elements(shape)

            draw_item_grid(renderer, AbstractContainerGUI.BORDER, self.gui_element_shape[0], self.gui_element_shape[1], shape)

    def update_gui_elements(self, shape):
        self.gui_element_shape = [self.root_x,
                                  self.root_y,
                                  shape[0]*AbstractContainerGUI.ITEM_CELL_SIZE + AbstractContainerGUI.BORDER * 2,
                                  shape[1]*AbstractContainerGUI.ITEM_CELL_SIZE + AbstractContainerGUI.BORDER * 2]

        self.gui_element_shape[0] = self.reference_point[0] - self.gui_element_shape[2]
        self.gui_element_shape[1] = self.reference_point[1]

        self.background_label_hover.x = self.gui_element_shape[0]
        self.background_label_hover.y = self.gui_element_shape[1]
        self.background_label_hover.width = self.gui_element_shape[2]
        self.background_label_hover.height = self.gui_element_shape[3]

    def get_item_grid_rect(self):
        return [self.gui_element_shape[0] + AbstractContainerGUI.BORDER,
                self.gui_element_shape[1] + AbstractContainerGUI.BORDER,
                self.gui_element_shape[2] - 2 * AbstractContainerGUI.BORDER,
                self.gui_element_shape[3] - 2 * AbstractContainerGUI.BORDER]

    @staticmethod
    def determine_item_draw_rect(rx, ry, item_shape, item_start_pos):
        i = item_start_pos[0]*AbstractContainerGUI.ITEM_CELL_SIZE + rx
        j = item_start_pos[1]*AbstractContainerGUI.ITEM_CELL_SIZE + ry
        w = item_shape[0]*AbstractContainerGUI.ITEM_CELL_SIZE
        h = item_shape[1]*AbstractContainerGUI.ITEM_CELL_SIZE
        return i, j, w, h

    def is_mouse_over_item_rect(self, i, j, w, h):
        return i < self.mouse_mem.mx < i+w and j < self.mouse_mem.my < j+h

    def execute(self, renderer):

        if self.gui_state == ContainerGUI.OPENED:

            # First check if we can draw anything due to the validity of the logic container
            if not self.container_logic.is_valid():
                return

            rx, ry, rw, rh = self.get_item_grid_rect()

            items = self.container_logic.get_items()

            for item in items.values():

                item_shape = item.get_shape()
                item_start_pos = item.get_start_position()


                i, j, w, h = self.determine_item_draw_rect(rx, ry, item_shape, item_start_pos)
                item_draw_rect = Rect(i, j, w, h)

                uid = item.get_uid()
                surface = self.item_resource_mapper.get_item_resource(item.get_tid())
                if surface is None:
                    surface = pygame.Surface((item_shape[0]*AbstractContainerGUI.ITEM_CELL_SIZE,
                                              item_shape[1]*AbstractContainerGUI.ITEM_CELL_SIZE))
                    surface.fill((255, 125, 0))

                # Handle the case that the item we want to draw currently is a dragged item
                if self.drag_drop_service.has_dragged_item():
                    dragged_item = self.drag_drop_service.get_dragged_item()
                    if uid == dragged_item.get_itemuid():
                        item_draw_rect = Rect(self.mouse_mem.mx, self.mouse_mem.my, w, h)
                        renderer.blit(surface, item_draw_rect)
                        continue

                # If there is no dragged item draw a border around the items when we hover over them
                if self.is_mouse_over_item_rect(i, j, w, h) and not self.drag_drop_service.has_dragged_item():
                    pygame.draw.rect(renderer, RED, item_draw_rect, 1)

                    # If furthermore the mouse button is down on this item
                    # we can request to put that item to a drag state (we already know that there is no dragged object)
                    if self.mouse_mem.mb1:
                        self.drag_drop_service.put_dragged_item(self, ItemDrag(item, self.mouse_mem.mx, self.mouse_mem.my))
                        # Adjust the rect so the item is directly drew as dragged
                        item_draw_rect = Rect(self.mouse_mem.mx, self.mouse_mem.my, w, h)
                    elif self.mouse_mem.mb3:
                        self.handle_right_mouse_click_on_item(item)
                    elif self.mouse_mem.mb2:
                        self.handle_middle_mouse_click_on_item(item)

                # If we got to this point just draw the item
                renderer.blit(surface, item_draw_rect)

                if self.wearing_manager is not None:
                    if self.wearing_manager.is_wearing(uid):
                        slot = self.wearing_manager.get_wearing_slot(uid)
                        surface = self.wearing_surface_slot_mapping[slot]
                        renderer.blit(surface, pygame.Rect(i, j, 32, 32))

                item_usages = item.get_num_uses()

                if item_usages > 0:
                    titleFont = pygame.font.Font('freesansbold.ttf', 20)
                    rendered_text = titleFont.render(str(item_usages), True, (0, 0, 0))
                    rendered_text_rect = rendered_text.get_rect()
                    rendered_text_rect.x = i+w-rendered_text_rect.width
                    rendered_text_rect.y = j+h-rendered_text_rect.height
                    renderer.blit(rendered_text, rendered_text_rect)

            for item in items.values():
                item_shape = item.get_shape()
                item_start_pos = item.get_start_position()
                i, j, w, h = self.determine_item_draw_rect(rx, ry, item_shape, item_start_pos)

                if self.mouse_mem.is_stable() and self.is_mouse_over_item_rect(i, j, w, h):
                    titleFont = pygame.font.Font('freesansbold.ttf', 16)
                    rendered_text = titleFont.render(str(item.get_name()), True, (0, 0, 0))
                    rendered_text_rect = rendered_text.get_rect()
                    rendered_text_rect.center = (self.mouse_mem.mx, self.mouse_mem.my - rendered_text_rect.height)
                    underground_rect = Rect(rendered_text_rect.x-1, rendered_text_rect.y-1, rendered_text_rect.width+2, rendered_text_rect.height+2)
                    pygame.draw.rect(renderer, WHITE, underground_rect)
                    pygame.draw.rect(renderer, BLACK, underground_rect, 1)
                    renderer.blit(rendered_text, rendered_text_rect)

            # If the DragDropService has an item but we don't have the mouse button anymore we call
            # the service to release it
            if self.drag_drop_service.has_dragged_item() and not self.mouse_mem.mb1:
                self.drag_drop_service.cancel_drag_drop()

            # At last we need to handle the case that there are currently drag and drop items above us
            if self.drag_drop_service.has_dragged_item():
                dragged_item = self.drag_drop_service.get_dragged_item()

                dx = self.mouse_mem.mx - rx
                dy = self.mouse_mem.my - ry

                pygame.draw.rect(renderer, GREEN, Rect(rx, ry, rw, rh), 1)

                if 0 < dx < rw and 0 < dy < rh:
                    xr = int(dx / AbstractContainerGUI.ITEM_CELL_SIZE)
                    yr = int(dy / AbstractContainerGUI.ITEM_CELL_SIZE)

                    s1, s2 = dragged_item.get_item().get_shape()

                    target_border_rect = Rect(xr*AbstractContainerGUI.ITEM_CELL_SIZE+rx,
                                              yr*AbstractContainerGUI.ITEM_CELL_SIZE+ry,
                                              s1*AbstractContainerGUI.ITEM_CELL_SIZE,
                                              s2*AbstractContainerGUI.ITEM_CELL_SIZE)
                    pygame.draw.rect(renderer, RED, target_border_rect, 1)

    def handle_right_mouse_click_on_item(self, item):
        pass

    def handle_middle_mouse_click_on_item(self, item):
        pass

    def get_container_logic(self):
        return self.container_logic

    def is_mouse_in_my_range(self):
        x_top, y_top, grid_width, grid_height = self.get_item_grid_rect()
        dx = self.mouse_mem.mx - x_top
        dy = self.mouse_mem.my - y_top
        return dx, dy, grid_height, grid_width, x_top, y_top

    def notify_accepted(self, item):
        print "Removing item from my container", item
        self.container_logic.remove_item_local(item.get_itemuid())

    def finish_drop(self, item):
        if self.gui_state == ContainerGUI.OPENED:
            x_top, y_top, grid_width, grid_height = self.get_item_grid_rect()
            dx = self.mouse_mem.mx - x_top
            dy = self.mouse_mem.my - y_top
            if 0 < dx < grid_width and 0 < dy < grid_height:
                xr = int(dx / AbstractContainerGUI.ITEM_CELL_SIZE)
                yr = int(dy / AbstractContainerGUI.ITEM_CELL_SIZE)

                shallow_item = item[1].get_item()
                mem_start_position = shallow_item.get_start_position()
                shallow_item.set_start_position((xr, yr))

                if self.container_logic.is_shape_valid([shallow_item]):
                    self.container_logic.add_local_item(shallow_item)
                    print "Item dropped on me:", xr, yr, shallow_item

                    self.client_socket_wrapper.send_moving_item_request(
                        item[0].get_container_logic().get_container_type(),
                        self.get_container_logic().get_container_type(),
                        shallow_item.get_uid(),
                        (xr, yr)
                    )
                    return True
                else:
                    shallow_item.set_start_position(mem_start_position)
        return False


class ContainerGUI(AbstractContainerGUI):

    def __init__(self, container_logic, main_gui, drag_drop_service, resource_manager, client_socket_wrapper):
        AbstractContainerGUI.__init__(self, WINDOWWIDTH-200, 400, container_logic, main_gui, drag_drop_service,
                                      resource_manager, client_socket_wrapper)

        self.client_socket_wrapper = client_socket_wrapper

    def send_close_command(self):
        self.client_socket_wrapper.send_close_normal_loot_container_command()

    def looting_toggle_command(self):
        if self.container_logic.is_container_open():
            self.client_socket_wrapper.send_close_normal_loot_container_command()
        else:
            self.client_socket_wrapper.send_open_normal_loot_container_command()


class CraftingGUI(AbstractContainerGUI):

    def __init__(self,  container_logic, main_gui, drag_drop_service, resource_manager, client_socket_wrapper):
        AbstractContainerGUI.__init__(self, 200, 200, container_logic, main_gui, drag_drop_service, resource_manager,
                                      client_socket_wrapper)

        self.client_socket_wrapper = client_socket_wrapper

        self.container_gui_craft_button = ButtonGUI('container_craft_button_%s' % self.container_logic.get_name(),
                                self.gui_element_shape,
                                caption="craft",
                                function=self.send_craft_command)

        self.container_gui_craft_button_enabled = True
        self.container_gui_craft_button.set_visible(False)

        main_gui.add(self.container_gui_craft_button)

    def send_craft_command(self):
        self.client_socket_wrapper.send_crafting_request()

    def send_close_command(self):
        self.client_socket_wrapper.send_close_crafting_container_command()

    def crafting_toggle_command(self):
        if self.container_logic.is_container_open():
            self.client_socket_wrapper.send_close_crafting_container_command()
        else:
            self.client_socket_wrapper.send_open_crafting_container_command()

    def set_all_gui_element_visible_to(self, state):
        AbstractContainerGUI.set_all_gui_element_visible_to(self, state)

        if hasattr(self, 'container_gui_craft_button'):
            self.container_gui_craft_button.set_visible(state)

    def update_gui_elements(self, shape):
        AbstractContainerGUI.update_gui_elements(self, shape)

        if hasattr(self, 'container_gui_craft_button'):
            self.container_gui_craft_button.x = self.background_label_hover.x
            self.container_gui_craft_button.y = self.background_label_hover.y + self.background_label_hover.height
            self.container_gui_craft_button.width = self.gui_element_shape[2]
            self.container_gui_craft_button.height = 30
            self.container_gui_craft_button.set_zorder(1)


class InventoryGUI(AbstractContainerGUI):

    def __init__(self,  container_logic, main_gui, drag_drop_service, resource_manager, client_socket_wrapper, wearing_manager):
        AbstractContainerGUI.__init__(self, 450, 250, container_logic, main_gui,
                                      drag_drop_service, resource_manager,
                                      client_socket_wrapper, wearing_manager=wearing_manager)

        self.client_socket_wrapper = client_socket_wrapper
        self.sound_engine = None

    def set_sound_engine(self, sound_engine):
        self.sound_engine = sound_engine

    def send_close_command(self):
        pass

    def back_pack_toggle_command(self):
        if self.container_logic.is_container_open():
            self.client_socket_wrapper.send_close_backpack_command()
        else:
            self.client_socket_wrapper.send_open_backpack_command()

    def toggle_visible_state_based_on_container_logic(self):
        if self.gui_state == AbstractContainerGUI.OPENED and not self.container_logic.is_container_open():
            self.sound_engine.play("backpack_closing")

        if self.gui_state == AbstractContainerGUI.CLOSED and self.container_logic.is_container_open():
            self.sound_engine.play("backpack_opening")

        AbstractContainerGUI.toggle_visible_state_based_on_container_logic(self)

    def handle_right_mouse_click_on_item(self, item):
        self.client_socket_wrapper.send_client_requests_wearing_item(item.item_uid)
