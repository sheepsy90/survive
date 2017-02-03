# -*- coding:utf-8 -*-
import json
from numpy import array
import os

from numpy.core.umath import sign

from common.AreaChangeSpot import AreaChangeSpot
from common.level.EnemyLoader import TiledEnemy
from common.level.TiledObject import TileObject
from common.level.TiledScript import TiledScript

class Layer(object):
    pass

    def __init__(self, layer_data):
        self.layer_data = layer_data

    def get_name(self):
        return self.layer_data[u'name']

    def get_data(self):
        return self.layer_data[u'data']

    def get_objects(self):
        return self.layer_data[u'objects']

    def get_zorder(self):
        if u'layer_' in self.layer_data[u'name']:
            return int(self.layer_data[u'name'].split("_")[1])
        else:
            raise EnvironmentError("You requested a zorder but this layer is not a zorder graphics layer!")


class Tileset(object):

    def __init__(self, tileset_data):
        self.tileset_data = tileset_data

        # Make some assertions
        assert self.tileset_data[u'tilewidth'] == 32
        assert self.tileset_data[u'tileheight'] == 32

    def get_name(self):
        return self.tileset_data[u'name']

    def get_asset_image_name(self):
        return self.tileset_data[u'image'].split("/")[-1]

    def get_firstgid(self):
        return self.tileset_data[u'firstgid']

    def get_image_dimensions(self):
        w, h = self.tileset_data[u'imagewidth'], self.tileset_data[u'imageheight']
        return w, h



class LevelTemplate(object):

    def __init__(self, identifier, size, layers, tilesets, atmospheric_data):
        self.identifier = identifier
        self.width, self.height = size
        self.layers = layers
        self.tilesets = tilesets
        self.coordinate_mapping = self.__get_tile_coordinate_mapping()
        self.atmospheric_data = atmospheric_data

    def get_size(self):
        return self.width, self.height

    def __get_tile_coordinate_mapping(self):
        mapping = {}
        for tileset in self.tilesets.values():
            first_gid = tileset.get_firstgid()
            asset_name = tileset.get_asset_image_name()

            width, height = tileset.get_image_dimensions()
            twidth, theight = width/32, height/32

            for i in range(twidth):
                for j in range(theight):
                    mapping[first_gid+j*twidth+i] = [asset_name, (i, j)]

        return mapping

    def get_coordinate_mapping(self):
        return self.coordinate_mapping

    def get_atmospheric_data(self):
        return self.atmospheric_data

    def get_level_layers(self):
        return self.layers

    def build_walk_map(self):
        """ This method returns a numpy array in the shape of the map where 1 indicates not accessible,
            0 means accessible """
        allowed_gid = self.tilesets[u'walkable_states'].get_firstgid()

        walk_layer = self.layers[u'Accessible']

        data = walk_layer.get_data()

        walk_matrix = array(data)
        walk_matrix = walk_matrix.reshape((self.height, self.width))
        walk_matrix -= allowed_gid

        return walk_matrix.transpose()

    def build_robot_follow_map(self):
        """ This method returns a numpy array in the shape of the map where 1 indicates not accessible,
            0 means accessible """
        robot_movement_layer = self.layers[u'RobotPathways']

        data = robot_movement_layer.get_data()

        robot_movement_layer = array(data)
        robot_movement_layer = sign(robot_movement_layer)
        robot_movement_layer = robot_movement_layer.reshape((self.height, self.width))

        return robot_movement_layer.transpose()

    def build_internal_scripts(self):
        objects = self.layers[u'Scripts'].get_objects()

        script_objects = []

        for i in range(len(objects)):
            obj = objects[i]

            # The normal objects
            to = TiledScript.from_dict(obj)

            script_objects.append(to)

        return script_objects

    def build_enemies(self):
        objects = self.layers[u'Enemies'].get_objects()

        enemy_objects = []

        for i in range(len(objects)):
            obj = objects[i]

            assert u'properties' in obj

            assert u'robot_type' in obj[u'properties']
            assert u'robot_count' in obj[u'properties']
            assert u'robot_script' in obj[u'properties']

            robot_type = int(obj[u'properties'][u'robot_type'])
            robot_count = int(obj[u'properties'][u'robot_count'])
            robot_script = obj[u'properties'][u'robot_script']

            if u'polyline' in obj:
                # Handle Polyline Stuff
                tile_list = TiledEnemy.calculate_tile_list_polyline(obj)
                te = TiledEnemy(tile_list, robot_type, robot_count, robot_script)
                enemy_objects.append(te)
            elif u'ellipse' in obj:
                tile_list = TiledEnemy.calculate_tile_list_ellipse(obj)
                te = TiledEnemy(tile_list, robot_type, robot_count, robot_script)
                enemy_objects.append(te)
            else:
                # Must be a rect
                tile_list = TiledEnemy.calculate_tile_list_rect(obj)
                te = TiledEnemy(tile_list, robot_type, robot_count, robot_script)
                enemy_objects.append(te)

        return enemy_objects

    def build_area_transitions(self):
        objects = self.layers[u'AreaTransitions'].get_objects()

        area_transitions = []

        for i in range(len(objects)):
            obj = objects[i]

            # Handle the Area Change Special Objects
            is_transition = u'area_transition' in obj.get(u'properties', {})

            if is_transition:
                acs = AreaChangeSpot.from_tiled_object(obj)
                area_transitions.append(acs)
                print "Added Area Change Spot: {}".format(acs)

        return area_transitions

    def build_objects(self):
        objects = self.layers[u'Objects'].get_objects()

        tiled_objects = []

        for i in range(len(objects)):
            obj = objects[i]

            # The normal objects
            to = TileObject.from_dict(obj)

            tile_data = self.coordinate_mapping[to.get_gid()]
            tile_data = tile_data[0], tile_data[1][0], tile_data[1][1]
            to.add_tile_data(tile_data)
            tiled_objects.append(to)

        # Check for double object ids
        obj_check_list = []
        for element in tiled_objects:
            obj_id = element.get_object_id()
            if obj_id in obj_check_list:
                assert False, "[EXIT] Error in Loading Level - Double Object ID - %s" % str(obj_id)
            else:
                obj_check_list.append(obj_id)

        return tiled_objects

    def get_identifier(self):
        return self.identifier


class LevelFactory():
    """ This class is responsible for leading a level file which is then used to construct an in game representation """

    @staticmethod
    def __load_level_data(level_file_path):
        with open(level_file_path, 'r') as f:
            return json.loads(f.read())

    def load_level_by_id(self, level_id, prefix=""):
        id_to_name_mapping = {
            1: os.path.abspath(prefix + 'resources/levels/after_tutorial_level.json'),
            3: os.path.abspath(prefix + 'resources/levels/level_tutorial.json'),
            4: os.path.abspath(prefix + 'resources/levels/level_01_left.json'),
            5: os.path.abspath(prefix + 'resources/levels/level_02_right.json'),
            6: os.path.abspath(prefix + 'resources/levels/common_room.json'),
            7: os.path.abspath(prefix + 'resources/levels/first_puzzle_test.json'),
            8: os.path.abspath(prefix + 'resources/levels/two_player_puzzle.json'),
        }
        name = id_to_name_mapping[level_id]
        return self.load_level(name)

    def load_level(self, level_file_path):
        # Fist of all get the level data from the json file
        level_data = self.__load_level_data(level_file_path)

        # Assume this map has some properties which are necessary for us
        assert u'properties' in level_data
        properties = level_data[u'properties']

        assert u'identifier' in properties
        identifier = properties[u'identifier']

        assert u'atmospheric_temperature' in properties
        assert u'atmospheric_type' in properties
        atmospheric_temperature = int(properties[u'atmospheric_temperature'])
        atmospheric_type = int(properties[u'atmospheric_type'])

        # Make some assertions about the layers
        assert u'layers' in level_data

        layers = [Layer(layer) for layer in level_data[u'layers']]
        layers = {layer.get_name(): layer for layer in layers}

        assert u'Accessible' in layers.keys()
        assert u'RobotPathways' in layers.keys()
        assert u'Objects' in layers.keys()
        assert u'AreaTransitions' in layers.keys()
        assert u'Scripts' in layers.keys()
        assert u'glass' in layers.keys()

        # Care about the tileset used
        assert u'tilesets' in level_data

        tilesets = [Tileset(t_data) for t_data in level_data[u'tilesets']]
        tilesets = {tileset.get_name(): tileset for tileset in tilesets}

        assert u'walkable_states' in tilesets.keys()

        # Get the Size of the Map
        assert u'width' in level_data
        assert u'height' in level_data

        width = level_data[u'width']
        height = level_data[u'height']

        return LevelTemplate(identifier, (width, height), layers, tilesets, [atmospheric_temperature, atmospheric_type])
