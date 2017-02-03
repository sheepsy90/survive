# -*- coding:utf-8 -*-
from numpy import nonzero, zeros, amax
from common.constants.ContainerConstants import ContainerConstants
from common.named_tuples import IDSystemStats
from server.validators.IdSystemValidator import IdSystemValidator
from server.world_objects.object_components.AbstractComponent import AbstractComponent
from server.world_objects.object_components.NpcComponent import NpcComponent


class Container(AbstractComponent):

    def __init__(self, refreshable, shape, container_type, searchable_type=None,
                 read_only=False, vanish_on_empty=False):
        AbstractComponent.__init__(self, AbstractComponent.CONTAINER_COMPONENT)
        self.refreshable = refreshable
        self.searchable_type = searchable_type

        assert container_type in [ContainerConstants.CONTAINER_TYPE_NORMAL,
                                  ContainerConstants.CONTAINER_TYPE_BACKPACK,
                                  ContainerConstants.CONTAINER_TYPE_CRAFTING]
        self.container_type = container_type

        # Define the Shape of the Container
        assert 0 < shape[0] <= 10
        assert 0 < shape[1] <= 10
        self.shape = shape

        self.content = None
        self.shape_mapping = None
        self.item_root_positions = None
        self.read_only = read_only
        self.vanish_on_empty = vanish_on_empty

    def is_empty(self):
        return len(self.item_root_positions.keys()) == 0

    def get_vanish_on_empty(self):
        return self.vanish_on_empty

    def get_searchable_type(self):
        return self.searchable_type

    def set_content(self, content):
        self.content = content

    def get_item_position(self, item_id):
        return self.item_root_positions.get(item_id, None)

    def position_content_within_container(self):
        self.content = {
            e.get_id(): e for e in self.content
        }

        result = self.find_placement_within_container()

        if result is not None:
            self.shape_mapping = result[0]
            self.item_root_positions = result[1]
            return True
        else:
            return None

    def prepare_content(self, empty=False):
        """ This method shall make sure that we have all items in here """
        if empty or self.content is None:
            self.content = []

        return self.position_content_within_container()


    def get_representation_for_crafting(self):
        representation = self.crop(self.shape_mapping)

        if representation is None:
            return ""

        def g(i):
            if i != 0:
                return str(self.content[i].get_type_id())
            else:
                return str(0)
        representation = [[g(i) for i in e] for e in representation]
        representation = "#".join([";".join(e) for e in representation])
        return representation

    def crop(self, m):
        xind, yind = nonzero(m)

        le = 0 if len(xind) == 0 else min(xind)
        re = 0 if len(xind) == 0 else max(xind)+1

        te = 0 if len(yind) == 0 else min(yind)
        be = 0 if len(yind) == 0 else max(yind)+1

        cutted = m[le:re:1, te:be:1]

        if cutted.shape == (0, 0):
            return None

        twod_list = [list(e) for e in cutted]

        return twod_list

    def build_matrix_mapping(self):
        self.shape_mapping = zeros(self.shape)

        for id in self.content:
            item = self.content[id]
            i, j = self.item_root_positions[id]
            it, jt = item.get_shape()
            it, jt = it+i, jt+j
            self.shape_mapping[i:it:1, j:jt:1] = item.get_id()

    def find_placement_within_container(self):
        """ This method finds a placement within the container and
            returns the x,y points for each object if feasible """

        # First sort all the items by height so we get a sense full positioning
        items_by_height = sorted(self.content.values(), key=lambda e: e.get_height())

        # Then create a numpy array with the shape and the size of the container
        container_array = zeros(self.shape)

        # Create a map to save the beginning coordinates for the items
        start_coordinates = {}

        for item in items_by_height:
            item_shape = item.get_shape()

            item_placed = False

            # TODO can be optimized
            for i in range(self.shape[0]):

                if item_placed:
                    break

                for j in range(self.shape[1]):
                        if container_array[i][j] == 0:

                            it = i+item_shape[0]
                            jt = j+item_shape[1]

                            if it > self.shape[0] or jt > self.shape[1]:
                                continue

                            # If only zeroes are in the sub-array that means that there is no item yet
                            if amax(container_array[i:it:1, j:jt:1]) == 0:
                                container_array[i:it:1, j:jt:1] = item.get_id()
                                start_coordinates[item.get_id()] = (i, j)
                                item_placed = True
                                break

            if not item_placed:
                return None

        return container_array, start_coordinates

    def get_item_by_id(self, item_id):
        if item_id not in self.content:
            return None
        else:
            return self.content[item_id]

    def remove_item(self, item):
        self.erase_shape_map_for_item(item)
        del self.content[item.get_id()]
        del self.item_root_positions[item.get_id()]

    def erase_shape_map_for_item(self, item):
        assert item.get_id() in self.content

        i, j = self.item_root_positions[item.get_id()]
        si, sj = item.get_shape()
        it, jt = i+si, j+sj
        self.shape_mapping[i:it:1, j:jt:1] = 0

    def put_item_if_fits(self, item, item_new_start_pos):

        if self.read_only:
            return False

        i, j = item_new_start_pos
        it, jt = item.get_shape()
        it, jt = i+it, j+jt

        if not(0 <= i and it <= self.shape[0] and 0 <= j and jt <= self.shape[1]):
            print i, j, it, jt
            return False

        cutted = self.shape_mapping[i:it:1, j:jt:1]
        lst = list(cutted.reshape(cutted.shape[0]*cutted.shape[1], 1))
        reduced = [e for e in lst if e != 0 and e != item.get_id()]

        if len(reduced) == 0:
            # We know that it fits in here but it could be that the item is already placed in this container
            if item.get_id() in self.content:
                # Item in here so we clear first before setting to new position
                self.erase_shape_map_for_item(item)
                self.shape_mapping[i:it:1, j:jt:1] = item.get_id()
            else:
                # Item is new so we just overwrite
                self.shape_mapping[i:it:1, j:jt:1] = item.get_id()
            self.item_root_positions[item.get_id()] = item_new_start_pos
            self.content[item.get_id()] = item

            return True
        else:
            return False

    def get_content(self):
        return self.content.values()

    def get_item_root_positions(self):
        return self.item_root_positions

    def get_container_shape(self):
        return self.shape

    def get_container_type(self):
        return self.container_type

    def shallow_clear(self):
        self.shallow_content = self.content
        self.shallow_shape_mapping = self.shape_mapping
        self.shallow_item_root_positions = self.item_root_positions

        self.content = None
        self.shape_mapping = None
        self.item_root_positions = None

        self.prepare_content(empty=True)

    def complete_clear(self):
        pass

    def set_shape(self, xs, ys):
        self.shape = [xs, ys]

    def restore(self):
        self.content = self.shallow_content
        self.shape_mapping = self.shallow_shape_mapping
        self.item_root_positions = self.shallow_item_root_positions

    def has_sufficient_id_card(self, guard_type,  guard_level):
        """ This method is checking whether the player has an id card in his bag which allows him to pass """

        system_stats = IdSystemValidator.create_id_system_stats(guard_type, guard_level)

        is_requirement_met = False

        for element in self.content.values():
            is_requirement_met |= IdSystemValidator.is_requirement_met(element.get_item_template(),
                                                                       id_system_stats=system_stats)

            if is_requirement_met:
                break

        return is_requirement_met
