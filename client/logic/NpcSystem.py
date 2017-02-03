# -*- coding:utf-8 -*-
import logging
from client.sound.ResourceManager import ResourceManager

logger = logging.getLogger(__name__)

class NPC():

    def __init__(self, npc_id, npc_name, character_tile_position, npc_text):
        self.npc_id = npc_id
        self.npc_name = npc_name
        self.character_tile_position = character_tile_position
        self.npc_text = npc_text

    def get_id(self):
        return self.npc_id

    def get_text(self):
        return self.npc_text

    def get_name(self):
        return self.npc_name

    def get_character_tile_position(self):
        return self.character_tile_position

    @staticmethod
    def parse(json_content):
        npc_id = json_content["id"]
        npc_name = json_content["name"]
        character_tile_position = json_content["character_tile_position"]
        npc_text = json_content["text"]
        return NPC(npc_id, npc_name, character_tile_position, npc_text)


class NpcSystem(object):

    def __init__(self):
        self.current_npc_id = None

        self.all_npc_dict = {npc.get_id(): npc for npc in self.load_all_npc()}
        self.guard_denies_access = []

    def interaction_with_npc_type(self, npc_id):
        if npc_id not in self.all_npc_dict:
            logger.error("Client tried to access an unknown NPC Id: {}".format(npc_id))

        if self.current_npc_id is not None:
            logger.error("Client tried to interact with NPC while already having one interaction NPC Id: {}"
                         .format(npc_id))

        self.current_npc_id = npc_id

    def get_current_npc(self):
        return self.all_npc_dict[self.current_npc_id]

    def has_current_npc(self):
        return self.current_npc_id is not None

    def close(self):
        self.current_npc_id = None

    def guard_denies_access(self, wo_id, xt, yt):
        self.guard_denies_access.append([wo_id, xt, yt])


    @staticmethod
    def load_all_npc():
        rm = ResourceManager()
        return [NPC.parse(e) for e in rm.load_json("npcs")["npcs"]]
