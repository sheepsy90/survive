# -*- coding:utf-8 -*-
from common.ItemTemplateTags import ItemTemplateTagConsistencyChecker
from common.constants.Directions import Directions
from common.named_tuples import NpcComponentProperties


class TileObject():

    def __init__(self, object_id, gid, xreal, yreal, properties):
        self.gid = gid
        self.xreal = xreal
        self.yreal = yreal
        self.tile_data = None
        self.object_id = object_id

        self.components = {}

        # TODO Build that into a dict based representation
        self.searchable = False
        self.initial_item_types = None
        self.searchable_type = None
        if u'searchable' in properties:
            self.searchable = True
            assert u'initial_content' in properties
            assert u'searchable_type' in properties
            self.initial_item_types = eval(properties[u'initial_content'])
            self.searchable_type = properties[u'searchable_type']

        self.stepable = False
        if u'stepable' in properties:
            self.stepable = True

        self.collidable = False
        if u'collidable' in properties:
            self.collidable = True

        self.usable = False
        self.usable_args = None
        if u'usable' in properties:
            self.usable = True
            self.usable_args = {key: properties[key] for key in properties if u'usable' in key}

        self.npc = False
        self.npc_properties = None
        if u'npc' in properties:
            self.npc = True
            npc_type = properties[u'npc_type']
            npc_is_guard = properties.get(u'npc_is_guard', False)
            npc_guard_type = properties.get(u'npc_guard_type', None)
            npc_guard_orientation = properties.get(u'npc_guard_orientation', None)
            npc_guard_level = properties.get(u'npc_guard_level', None)
            self.npc_properties = NpcComponentProperties(npc_type, npc_is_guard, npc_guard_type,
                                                         npc_guard_orientation, npc_guard_level)

        if u'laser' in properties:
            self.components[u'laser'] = {}

            assert u'laser_distance' in properties
            self.components[u'laser'][u'laser_distance'] = properties.get(u'laser_distance', 0)

            assert u'laser_direction' in properties
            self.components[u'laser'][u'laser_direction'] = properties.get(u'laser_direction', Directions.DOWN)

        if u'mine' in properties:
            self.components[u'mine'] = {}

            assert u'mine_radius' in properties
            self.components[u'mine'][u'mine_radius'] = properties.get(u'mine_radius', None)

        self.tags = []
        if u'tags' in properties:
            values = properties[u'tags']
            splitted_tags = values.split(" ")
            ItemTemplateTagConsistencyChecker.check_input_list(splitted_tags)
            self.tags = splitted_tags

    def has_component_key(self, component_key):
        return self.components.__contains__(component_key)

    def get_component_data(self, component_key):
        return self.components.get(component_key)

    def get_tags(self):
        return {e: True for e in self.tags}

    def get_usable_flags(self):
        return self.usable, self.usable_args

    def get_npc_flags(self):
        return self.npc, self.npc_properties

    def get_searchable_flags(self):
        return self.searchable, self.initial_item_types, self.searchable_type

    def get_stepable_flag(self):
        return self.stepable

    def get_collidable_flag(self):
        return self.collidable

    def get_gid(self):
        return self.gid

    def get_position(self):
        return self.xreal, self.yreal

    def get_tile_data(self):
        return self.tile_data

    def add_tile_data(self, tile_data):
        tileset, px, py = tile_data
        self.tile_data = tileset[0:-4], px, py

    def set_object_id(self, obj_id):
        self.object_id = obj_id

    def get_object_id(self):
        return self.object_id

    def __repr__(self):
        return "Tile Object %i with tile data %s and position (%i, %i)" % (self.object_id, str(self.tile_data), self.xreal, self.yreal)

    @staticmethod
    def from_dict(dictionary):
        assert u'name' in dictionary
        assert u'type' in dictionary
        assert u'y' in dictionary
        assert u'x' in dictionary
        assert u'properties' in dictionary
        assert u'rotation' in dictionary

        properties = dictionary[u'properties']
        object_id = int(dictionary[u"type"])

        if u'gid' not in dictionary:
            assert u'script' in properties
            gid = 0
            return TileObject(object_id, gid, 0, 0, properties)

        else:
            gid = dictionary[u'gid']

            x_real = dictionary[u"x"]
            y_real = dictionary[u"y"]
            rotation = dictionary[u"rotation"]

            assert x_real == int(x_real), "The object with id %i is not placed properly" % object_id
            assert y_real == int(y_real), "The object with id %i is not placed properly" % object_id
            assert rotation == 0

            return TileObject(object_id, gid, x_real, y_real, properties)


