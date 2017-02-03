# -*- coding:utf-8 -*-
import json
import os


class ItemResourceMapper():

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager

        with open(os.path.abspath("resources/id_image_mapping.json"), 'r') as f:
            data = json.loads(f.read())

        self.dummy = self.resource_manager.load_image('items/dummy')

        self.map = {
            int(e): self.load(data[e]) for e in data
        }

    def load(self, path):
        try:
            return self.resource_manager.load_image(path)
        except Exception as e:
            print "[ERROR] Could not find image", path

    def get_item_resource(self, key):
        if key not in self.map:
            return self.dummy
        else:
            return self.map[key]