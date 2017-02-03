# -*- coding:utf-8 -*-
from client.config import CELLSIZE

class MarkerObject():

    def __init__(self,  anim_id, posx, posy):
        self.anim_id = anim_id
        self.posx = posx
        self.posy = posy

    def get_position(self):
        return self.posx, self.posy

    def get_animation_type(self):
        return self.anim_id

class MarkerLogic():

    def __init__(self):
        self.marker_objects = {}

    def get_objects(self):
        return self.marker_objects.values()

    def add_marker_to_show(self, unique_id, anim_id, posx, posy):
        self.marker_objects[unique_id] = MarkerObject(anim_id, posx, posy)

    def delete_marker_to_show(self, key):
        if key in self.marker_objects:
            del self.marker_objects[key]


class BasicMarkerDrawer():

    def __init__(self, resource_manager, marker_logic):
        self.resource_manager = resource_manager
        self.marker_logic = marker_logic

        a = self.resource_manager.load_animation("arrow_on_spot_red", 8, [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], loop=True)
        a.play()

        self.marker_animations_mapping = {
            "arrow": a
        }

    def draw(self, renderer, level, offset):

        marker_objects = self.marker_logic.get_objects()

        me = level.get_player_manager().get_me()
        d, posx, posy = me.get_position()

        for obj in marker_objects:
            px, py = obj.get_position()

            dx = px - posx
            dy = py - posy

            if -11 <= dx <= 11 and -11 <= dy <= 11:
                dx = dx + 9
                dy = dy + 9

                anim_id = obj.get_animation_type()

                assert anim_id in self.marker_animations_mapping

                animation = self.marker_animations_mapping[anim_id]

                x = (dx + offset) * CELLSIZE
                y = (dy + offset) * CELLSIZE
                animation.blit(renderer, (x, y))