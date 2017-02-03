# -*- coding:utf-8 -*-
from numpy import zeros
from common.constants.ContainerConstants import ContainerConstants


class AbstractClientContainerManager():

    def __init__(self, name, container_type, shape=None):
        self.name = name
        self.shape = shape
        self.container_client_representation = {}
        self.container_opened = False
        self.container_type = container_type

    def get_name(self):
        return self.name

    def get_items(self):
        real_return = {key: value for key, value in self.container_client_representation.items() if not value.is_marked_for_deletion()}
        discard = [key for key, value in self.container_client_representation.items() if value.is_marked_for_deletion()]
        [self.remove_item_local(key) for key in discard]
        return real_return

    def set_closed(self):
        self.container_opened = False

    def set_opened(self):
        self.container_opened = True

    def clear_items(self):
        self.container_client_representation = {}

    def is_container_open(self):
        return self.container_opened

    def remove_item_local(self, uid):
        del self.container_client_representation[uid]

    def add_local_item(self, shallow_item):
        self.container_client_representation[shallow_item.get_uid()] = shallow_item

    def add_shallow_item(self, shallow_item):
        self.container_client_representation[shallow_item.get_uid()] = shallow_item

    def get_item_by_id(self, uid):
        return self.container_client_representation[uid]

    def set_shape(self, shape):
        self.shape = shape

    def is_valid(self):
        return self.shape is not None

    def is_shape_valid(self, additional_items=[]):
        assert self.shape is not None
        reference_array = zeros(self.shape)
        for item in self.container_client_representation.values() + additional_items:
            w, h = item.get_shape()
            itemid = item.get_uid()
            sx, sy = item.get_start_position()

            if not (0 <= sx+w <= self.shape[0] and 0 <= sy+h <= self.shape[1]):
                return False

            cutted = reference_array[sx:sx+w:1, sy:sy+h:1]

            lst = list(cutted.reshape(cutted.shape[0]*cutted.shape[1], 1))
            reduced = [e for e in lst if e != 0 and e != itemid]

            if len(reduced) > 0:
                return False
            else:
               reference_array[sx:sx+w:1, sy:sy+h:1] = itemid

        return True

    def get_shape(self):
        return self.shape

    def get_container_type(self):
        return self.container_type

    def clear(self):
        self.container_client_representation = {}


class LootingContainerManager(AbstractClientContainerManager):
    """ This class holds the game logic for the container system and therefore is accessed by the
        graphics to display that """

    def __init__(self):
        AbstractClientContainerManager.__init__(self, "LootingContainerManager", container_type=ContainerConstants.CONTAINER_TYPE_NORMAL)
        self.current_go_uid = None

    def open_container(self, go_uid, shape):
        # Container IDs
        self.current_go_uid = go_uid
        self.set_shape(shape)
        self.set_opened()

    def close_container(self):
        self.current_go_uid = None
        self.set_closed()
        self.clear_items()

class BackpackContainerManager(AbstractClientContainerManager):
    """ This class holds the game logic for the container system and therefore is accessed by the
        graphics to display that """

    def __init__(self):
        AbstractClientContainerManager.__init__(self, "BackpackContainerManager", container_type=ContainerConstants.CONTAINER_TYPE_BACKPACK)

    def open(self, shape):
        self.set_shape(shape)
        self.set_opened()

    def close(self):
        self.set_closed()
        self.clear_items()

class CraftingContainerManager(AbstractClientContainerManager):
    """ This class holds the game logic for the container system and therefore is accessed by the
        graphics to display that """

    def __init__(self):
        AbstractClientContainerManager.__init__(self, "CraftingContainerManager", container_type=ContainerConstants.CONTAINER_TYPE_CRAFTING)

    def open(self, shape):
        self.set_shape(shape)
        self.set_opened()

    def close(self):
        self.set_closed()
        self.clear_items()
