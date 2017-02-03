# -*- coding:utf-8 -*-
from common.constants.ContainerConstants import ContainerConstants


class ContainerOpenObject():

    def __init__(self):
        self.inventory = None
        self.crafting = None
        self.loot_container = None

    def set_crafting_container(self, container):
        self.crafting = container

    def set_backpack_container(self, container):
        self.inventory = container

    def set_looting_container(self, container):
        self.loot_container = container

    def delete_crafting_container(self):
        self.crafting = None

    def delete_backpack_container(self):
        self.inventory = None

    def delete_looting_container(self):
        self.loot_container = None

    def get_by_container_type(self, container_type):
        if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
            return self.loot_container
        elif container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
            return self.inventory
        elif container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
            return self.crafting

    def get_loot_container(self):
        return self.loot_container

    def get_crafting_container(self):
        return self.crafting

    def get_inventory_container(self):
        return self.inventory

    def is_empty(self):
        return self.inventory is None and self.crafting is None and self.loot_container is None

    def __repr__(self):
        return "I: %s, C: %s, L: %s" % (self.inventory, self.crafting, self.loot_container)

class ContainerOpenedMemorizeService():

    def __init__(self):
        self.opened_containers = {}

        self.opened_searchable_spots = set()

    def is_container_already_in_use(self, container):
        return container.get_parent_object_id() in self.opened_searchable_spots

    def set_container_for_player_opened(self, player, container):
        assert player is not None
        assert container is not None

        container_type = container.get_container_type()
        player_id = player.get_id()

        if player_id not in self.opened_containers:
            container_object = ContainerOpenObject()
            self.opened_containers[player_id] = container_object
        else:
            container_object = self.opened_containers[player_id]

        if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
            container_object.set_looting_container(container)
            self.opened_searchable_spots.add(container.get_parent_object_id())
        elif container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
            container_object.set_backpack_container(container)
        elif container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
            container_object.set_crafting_container(container)

        print self.opened_containers

    def remove_all_open_containers_for_player(self, player):
        """ Handle the case that a player e.g. logs off and then we need to clear this and handle things """
        if player.get_id() in self.opened_containers:
            del self.opened_containers[player.get_id()]

    def close_container_for_player(self, player, container):
        assert player is not None
        assert container is not None

        container_type = container.get_container_type()
        player_id = player.get_id()

        if player_id not in self.opened_containers:
            return

        container_object = self.opened_containers[player_id]

        if container_type == ContainerConstants.CONTAINER_TYPE_NORMAL:
            self.opened_searchable_spots.remove(container_object.get_loot_container().get_parent_object_id())
            container_object.delete_looting_container()
        elif container_type == ContainerConstants.CONTAINER_TYPE_BACKPACK:
            container_object.delete_backpack_container()
        elif container_type == ContainerConstants.CONTAINER_TYPE_CRAFTING:
            container_object.delete_crafting_container()

        if container_object.is_empty():
            del self.opened_containers[player_id]

    def get_loot_container_by_player(self, player):
        assert player is not None

        player_id = player.get_id()

        if player_id in self.opened_containers:
            container_object = self.opened_containers[player.get_id()]
            container = container_object.get_loot_container()
            return container

    def has_open_container(self, player):
        assert player is not None
        player_id = player.get_id()

        return player_id in self.opened_containers

    def has_open_crafting_container(self, player):
        assert player is not None
        player_id = player.get_id()

        if player_id not in self.opened_containers:
            return False

        container_object = self.opened_containers[player_id]
        crafting_container = container_object.get_crafting_container()

        return crafting_container is not None

    def has_open_inventory_container(self, player):
        assert player is not None
        player_id = player.get_id()

        if player_id not in self.opened_containers:
            return False

        container_object = self.opened_containers[player_id]
        inventory_container = container_object.get_inventory_container()

        return inventory_container is not None

    def get_both_containers_open(self, player, container_type_from, container_type_to):
        assert player is not None
        player_id = player.get_id()

        if player_id in self.opened_containers:
            container_object = self.opened_containers[player.get_id()]
            container_from = container_object.get_by_container_type(container_type_from)
            container_to = container_object.get_by_container_type(container_type_to)

            if container_from is None or container_to is None:
                return None
            else:
                return container_from, container_to

