# -*- coding:utf-8 -*-
from numpy import array
import time

from client.local_objects.ClientPlayerManager import ClientPlayerManager
from client.logic.HealthModifierManager import HealthModifierManager


class ClientObject():

    def __init__(self, area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload):
        self.area_id = area_id
        self.object_id = object_id
        self.tileset = tileset
        self.tposx = tposx
        self.tposy = tposy
        self.eposx = eposx
        self.eposy = eposy
        self.object_id = object_id
        self.visible = visible
        self.type = type
        self.payload = payload

    def is_visible(self):
        return self.visible

    def get_position(self):
        return self.eposx, self.eposy

    def get_object_id(self):
        return self.object_id

    def get_tileset_infos(self):
        return self.tileset, self.tposx, self.tposy

    def has_payload(self):
        return len(self.payload.keys()) > 0

    def get_payload(self):
        return self.payload

class ObjectManager(object):

    def __init__(self):
        self.objects = {}
        self.stepables_states = {}

    def add_to_objects(self, area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload):
        # TODO - Use the area id as an identifier maybe too
        co = ClientObject(area_id, object_id, tileset, tposx, tposy, eposx, eposy, visible, type, payload)
        self.objects[object_id] = co

    def remove(self, area_id, object_id):
        if object_id in self.objects:
            self.objects.__delitem__(object_id)

    def update_stepable_object(self, world_object_id, active):
        self.stepables_states[world_object_id] = bool(active)

    def get_stepable_values(self):
        return self.stepables_states

    def get_objects(self):
        return self.objects.values()


class AtmosphericSystem(object):

    def __init__(self):
        self.temperature = 10
        self.atmospheric_type = 0

    def set_temperature(self, temperature):
        self.temperature = temperature

    def set_atmospheric_type(self, atmospheric_type):
        self.atmospheric_type = atmospheric_type

    def get_atmospheric_type(self):
        return self.atmospheric_type

class ClientEnemyManager():

    def __init__(self):
        self.enemies = {}
        self.destroyed_enemies = {}
        self.attacking_enemies = {}

    def update_enemy(self, enemy_id, d, x, y, current_life, max_life):
        if current_life == 0 and enemy_id not in self.destroyed_enemies:
            self.destroyed_enemies[enemy_id] = time.time()

        self.enemies[enemy_id] = [enemy_id, d, x, y, current_life, max_life]

    def enemy_starts_attacking(self, enemy_id):
        self.attacking_enemies[enemy_id] = time.time()

    def remove_attacking_enemy(self, enemy_id):
        self.attacking_enemies.__delitem__(enemy_id)

    def get_enemies_attacking(self):
        return self.attacking_enemies

    def get_enemies(self):
        return self.enemies.values()

    def get_destroyed(self):
        return self.destroyed_enemies

class ClientBulletManager():

    def __init__(self):
        self.sound_engine = None
        self.active_bullets = {}
        self.in_destruction_bullets = {}

    def set_sound_engine(self, sound_engine):
        self.sound_engine = sound_engine

    def add_bullet(self, bullet_id, x, y):
        self.active_bullets[bullet_id] = [x, y]

    def bullet_destroyed(self, bullet_id):
        self.in_destruction_bullets[bullet_id] = time.time()

    def get_bullet_infos(self):
        return self.active_bullets, self.in_destruction_bullets

    def remove_bullet(self, bullet_id):
        if bullet_id in self.active_bullets:
            del self.active_bullets[bullet_id]
        if bullet_id in self.in_destruction_bullets:
            del self.in_destruction_bullets[bullet_id]

class FullClientLevel():

    def __init__(self, identifier, size, layers, tile_coordinate_mapping, walk_map):
        self.identifier = identifier
        self.size = size
        width, height = size

        graphic_layers = [layer for layer in layers.values() if 'layer' in layer.get_name()]

        self.graphic_layers = {
            layer.get_zorder(): array(layer.get_data()).reshape((height, width)).transpose() for layer in graphic_layers
        }

        robot_guidance_data = layers[u'RobotPathways'].get_data()
        glass_data = layers[u'glass'].get_data()

        self.robot_guidance_data_np = array(robot_guidance_data).reshape((height, width)).transpose()
        self.glass_data_np = array(glass_data).reshape((height, width)).transpose()

        self.walk_map = walk_map

        self.tile_coordinate_mapping = tile_coordinate_mapping

        self.client_player_manager = ClientPlayerManager()
        self.atmospheric_system = AtmosphericSystem()
        self.health_modifier_manager = HealthModifierManager()
        self.object_manager = ObjectManager()
        self.flashlight_on = False
        self.client_enemy_manager = ClientEnemyManager()
        self.bullet_manager = ClientBulletManager()

    def get_graphcis_zorder_layers(self):
        return self.graphic_layers

    def get_robot_guidance_data(self):
        return self.robot_guidance_data_np

    def get_glass_render_data(self):
        return self.glass_data_np

    def get_bullet_manager(self):
        return self.bullet_manager

    def get_client_enemy_manager(self):
        return self.client_enemy_manager

    def get_size(self):
        return self.size

    def get_tile_mapping(self):
        return self.tile_coordinate_mapping

    def get_player_manager(self):
        return self.client_player_manager

    def get_atmospheric_system(self):
        return self.atmospheric_system

    def get_walk_map(self):
        return self.walk_map

    def flashlight_enabled(self):
        return self.flashlight_on

    def toggle_flashlight(self):
        self.flashlight_on = not self.flashlight_on

    def get_object_manager(self):
        return self.object_manager

    def get_health_modifier_manager(self):
        return self.health_modifier_manager