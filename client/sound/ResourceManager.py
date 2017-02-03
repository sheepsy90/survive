# -*- coding:utf-8 -*-
import json
import os
import pygame
import time
from client.lib import pyganim


class Resource(object):

    def __init__(self, prefix, image_key, tile_size):
        self.tile_size = tile_size
        self.image_key = image_key
        self.image = pygame.image.load('%s%s.png' % (prefix, image_key))
        self.last_accessed = time.time()

    def get_subsurface(self, x, y):
        self.last_accessed = time.time()
        r = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
        subsurf = self.image.subsurface(r)
        #pygame.image.save(subsurf, '%s_%i_%i.png' % (self.image_key, x, y))
        return subsurf

    def get_last_accessed(self):
        return self.last_accessed

    def get_key(self):
        return self.image_key


class ResourceManager(object):
    """ The Ressource Manager shall create tiles from the graphic images whenever needed """

    def __init__(self):
        self.graphics_prefix = 'resources/graphics/'
        self.json_prefix = 'resources/json/'
        self.num_images_to_hold = 30
        self.resources_loaded = {}
        self.history = []

    def load_image_tile(self, resource_key, x, y, tile_size=32):
        if resource_key in self.resources_loaded.keys():
            resource = self.resources_loaded[resource_key]
        else:
            print "Creating new Resource"
            resource = Resource(self.graphics_prefix, resource_key, tile_size=tile_size)
            self.put_in_resource_dict(resource)

        return resource.get_subsurface(x, y)

    def load_image(self, name):
        return pygame.image.load(os.path.abspath('%s%s.png') % (self.graphics_prefix, name))

    def load_animation(self, animation_name, size, lst_times, loop=False, tile_size=32):
        parameter = []
        for i in range(size):
            surface = self.load_image_tile(animation_name, i, 0, tile_size)
            parameter.append((surface, lst_times[i]))
        return pyganim.PygAnimation(parameter, loop=loop)

    def put_in_resource_dict(self, resource):
        # Delete the one that was used the most in the past if we exceed the number of images in memory
        if len(self.resources_loaded.keys()) >= self.num_images_to_hold:
            all_resources = self.resources_loaded.values()
            all_resources = sorted(all_resources, key=lambda res: res.get_last_accessed())
            key_to_delete = all_resources[0].get_key()
            del self.resources_loaded[key_to_delete]

        # Add the new image
        self.resources_loaded[resource.get_key()] = resource

        # Log that due to its importance
        print "[ResourceManager] Loaded %s into memory!" % resource.get_key()

    def load_json(self, name):
        try:
            with open(os.path.abspath('{}{}.json'.format(self.json_prefix, name))) as f:
                return json.loads(f.read())
        except Exception as e:
            print e
            raise Exception("Could not parse requested JSON File {}".format(name))
