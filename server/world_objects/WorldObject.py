# -*- coding:utf-8 -*-


class WorldObject():
    """ This is the class defining an general objects in the level which stand around and have certain properties """

    def __init__(self, area_id, object_id, tile_info, posx, posy):
        self.area_id = area_id
        self.object_id = object_id
        self.tile_info = tile_info
        self.exact_posx = posx
        self.exact_posy = posy
        self.components = {}
        self.tags = {}
        self.visible = True

        self.fx = (self.exact_posx+16) / 32
        self.fy = (self.exact_posy-1) / 32

    def get_middle_foot_point(self):
        # TODO Build a real test for that stuff because its likly to break else
        return self.fx, self.fy

    def get_object_id(self):
        return self.object_id

    def get_area_id(self):
        return self.area_id

    def get_tile_info(self):
        return self.tile_info

    def get_exact_position(self):
        return self.exact_posx, self.exact_posy

    def is_visible(self):
        return self.visible

    def set_visible(self, value):
        if value != self.visible:
            self.visible = value
            return True
        return False

    def add_component(self, component):
        self.components[component.get_property_name()] = component
        component.set_parent(self)

    def get_component(self, component_name):
        if component_name in self.components:
            return self.components[component_name]

    def has_component(self, component_name):
        return component_name in self.components

    def get_component_keys(self):
        return self.components.keys()

    def has_tag(self, tag):
        return tag in self.tags

    def add_tag(self, tag):
        self.tags[tag] = True

    def remove_tag(self, tag):
        self.tags.__delitem__(tag)

    def set_tag_set(self, tag_set):
        self.tags = tag_set

    def get_payload(self):
        """ This is a generic method calling all the components and putting in the additional information that
            is provided by the components. This is the first test of the way of transporting additional information
            to the client about the world object - this should return a dictionary with the keys of the Components and
            the payload inside - it will be transported as JSON."""
        components_payload = {}

        for key, value in self.components.items():
            payload_result = value.get_payload()
            if payload_result is not None:
                components_payload[key] = payload_result

        return components_payload


    def __repr__(self):
        return "ObjId: %s - AreaId: %s"  % (str(self.object_id), str(self.area_id))