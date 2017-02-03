# -*- coding:utf-8 -*-
import logging
from server.constants.constans import USABLE_SCRIPT_MAPPING
from server.world_objects.WorldObject import WorldObject
from server.world_objects.object_components.MineComponent import MineComponent
from server.world_objects.object_components.AbstractComponent import AbstractComponent
from server.world_objects.object_components.LaserComponent import LaserComponent
from server.xmlrpc_services.crafting.CraftingServiceClient import CraftingServiceClient
from server.xmlrpc_services.items.ItemServiceClient import ItemServiceClient
from server.world_objects.object_components.CollidableComponent import CollidableComponent
from server.world_objects.object_components.ContainerComponent import Container
from server.world_objects.object_components.NpcComponent import NpcComponent
from server.world_objects.object_components.StepableComponent import StepableComponent
from server.world_objects.object_components.UsableComponent import UsableComponent

import errno
from socket import error as socket_error

from common.constants.ContainerConstants import ContainerConstants

logger = logging.getLogger(__name__)


class WorldObjectManager(object):
    """ This is the WorldObjectManager which is necessary to handle all the world object related stuff.
        In detail that is mainly the thing handling the components that can be attached to a world object.
        This is furthermore extracting a lot of code from the FullServerLevel. """
    
    ALLOWED_COMPONENTS = [AbstractComponent.COLLIDABLE_COMPONENT,
                          AbstractComponent.CONTAINER_COMPONENT,
                          AbstractComponent.NPC_COMPONENT,
                          AbstractComponent.STEPABLE_COMPONENT,
                          AbstractComponent.USABLE_COMPONENT,
                          AbstractComponent.MINE_COMPONENT,
                          AbstractComponent.LASER_COMPONENT]

    def __init__(self, level_identifier):
        self.level_identifier = level_identifier

        self.crafting_service_client = CraftingServiceClient()
        self.item_service_client = ItemServiceClient()

        # GameObject related stuff
        self.objects = {}

        self.components_cache = {}

        for allowed_component in WorldObjectManager.ALLOWED_COMPONENTS:
            self.components_cache[allowed_component] = {}

        self.object_id_counter = 0

    def add_object(self, game_object):
        """ This methods adds a kind of object to the map which can be in various states and so on - its
            almost surely represented by a tile within the client but we don't really need that here in the
            server """
        self.objects[game_object.get_object_id()] = game_object
        self.add_components_to_cache(game_object.get_object_id())

    def create_world_object(self, logical_x, logical_y):
        new_object_id = self.get_new_object_id()
        px_new = 32 * logical_x
        py_new = 32 * logical_y + 31
        wo = WorldObject(self.level_identifier, new_object_id, (u'searchables', 0, 1), px_new, py_new)
        self.objects[new_object_id] = wo

        logger.info("Created new WorldObject %s" % str(wo))
        return wo

    def delete_world_object(self, world_object):
        self.remove_components_from_cache(world_object.get_object_id())
        self.objects.__delitem__(world_object.get_object_id())

    def get_new_object_id(self):
        self.object_id_counter += 1
        return self.object_id_counter

    def get_objects(self):
        return self.objects.values()

    def get_world_object_by_id(self, idx):
        return self.objects.get(idx, None)

    def add_components_to_cache(self, object_id):
        """ This method deletes all the components for a given object id from the components cache. """
        game_object = self.objects[object_id]

        for key in game_object.get_component_keys():
            logger.info("Adding Component {} to Component Cache for ObjId {}".format(key, object_id))
            self.components_cache[key][object_id] = game_object

    def remove_components_from_cache(self, object_id):
        """ This method deletes all the components for a given object id from the components cache. """
        print self.objects
        game_object = self.objects[object_id]

        for key in game_object.get_component_keys():
            logger.info("Removing Component {} from the Component Cache for ObjId {}".format(key, object_id))
            self.components_cache[key].__delitem__(object_id)

    def load_searchable_component(self, tile_object, world_object):
        searchable, initial_info, searchable_type = tile_object.get_searchable_flags()
        if searchable:
            c = Container(refreshable=True, shape=(5, 5), container_type=ContainerConstants.CONTAINER_TYPE_NORMAL,
                          searchable_type=searchable_type)
            try:
                if len(initial_info) > 0:
                    content = []
                    for element in initial_info:
                        item_type, count = element
                        item_template = self.crafting_service_client.get_item_template(item_type)
                        items = self.item_service_client.create_multiple_items(item_template, count)
                        for item in items:
                            content.append(item)
                    c.set_content(content)
                    assert c.position_content_within_container()
            except AssertionError:
                raise ValueError("Initial Content to large for container")
            except socket_error as serr:
                if serr.errno != errno.ECONNREFUSED:
                    raise serr
                else:
                    logger.warn("Could not reach the Crafting or Item Service!")

            world_object.add_component(c)

    def load_steppable_component(self, tile_object, world_object):
        stepable = tile_object.get_stepable_flag()
        if stepable:
            s = StepableComponent()
            world_object.add_component(s)

    def load_collidable_component(self, tile_object, world_object):
        collidable = tile_object.get_collidable_flag()
        if collidable:
            c = CollidableComponent()
            world_object.add_component(c)

    def load_npc_component(self, tile_object, world_object):
        npc, npc_properties = tile_object.get_npc_flags()
        if npc:
            c = NpcComponent(npc_properties)
            world_object.add_component(c)

    def load_usable_component(self, server_level, tile_object, world_object):
        usable, usable_args = tile_object.get_usable_flags()
        if usable:
            assert u'usable_script' in usable_args
            script = usable_args[u'usable_script']
            params = {key.split("_")[2]: usable_args[key] for key in usable_args if u'usable_param_' in key}
            initialized_script = USABLE_SCRIPT_MAPPING.get(script)(server_level, world_object, params)
            u = UsableComponent(initialized_script)
            world_object.add_component(u)


    def build_objects(self, server_level, objects, ):
        """ This method gets the tiled objects that are originated at the level loader.
            Those are transformed to internal WorldObjects which have the components attached
        """

        # Create a list of object ids that are already in use
        object_ids_in_use = []

        for tile_object in objects:
            object_id = tile_object.get_object_id()
            object_ids_in_use.append(object_id)
            tile_data = tile_object.get_tile_data()
            posx, posy = tile_object.get_position()

            world_object = WorldObject(self.level_identifier, object_id, tile_data, posx, posy)

            tags = tile_object.get_tags()
            world_object.set_tag_set(tags)

            # Load all the components that could be attached to a world object
            self.load_searchable_component(tile_object, world_object)
            self.load_steppable_component(tile_object, world_object)
            self.load_collidable_component(tile_object, world_object)
            self.load_npc_component(tile_object, world_object)
            self.load_usable_component(server_level, tile_object, world_object)
            self.load_laser_component(tile_object, world_object)
            self.load_mine_component(tile_object, world_object)

            # Add the object which implicitly also updates the Components Cache
            self.add_object(world_object)

        if len(object_ids_in_use) != 0:
            self.object_id_counter = max(object_ids_in_use)
        else:
            self.object_id_counter = 1

    def initialize_usable_scripts(self):
        # The Script Initialization is done after the complete set up so we don't run into
        # internal access problems
        for world_object in self.components_cache[AbstractComponent.USABLE_COMPONENT].values():
            world_object.get_component(AbstractComponent.USABLE_COMPONENT).get_script().initialize()

    def get_values_from_component_cache(self, component_key):
        return self.components_cache[component_key].values()

    def load_laser_component(self, tile_object, world_object):
        if tile_object.has_component_key(u'laser'):

            data = tile_object.get_component_data(u'laser')

            direction = data[u'laser_direction']
            distance = data[u'laser_distance']

            c = LaserComponent(distance, direction)
            world_object.add_component(c)

    def load_mine_component(self, tile_object, world_object):
        if tile_object.has_component_key(u'mine'):

            data = tile_object.get_component_data(u'mine')

            radius = data.get(u'mine_radius', 1)

            c = MineComponent(radius)
            world_object.add_component(c)




