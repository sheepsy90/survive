# -*- coding:utf-8 -*-
from client.local_objects.PlayerModel import PlayerModel


class ClientPlayerManager(object):

    def __init__(self):
        self.players = {}
        self.me = None

    def add_new_player_position(self, player_id, player_name, position, is_moving, is_me):
        if player_id not in self.players:
            self.players[player_id] = PlayerModel(player_id, player_name, position, is_moving)
        else:
            self.players[player_id].update_position(position, is_moving)

        if is_me:
            self.me = self.players[player_id]

    def has_me(self):
        return self.me is not None

    def get_players(self):
        return self.players.values()

    def remove_player(self, name):
        print "REMOVE PLAYER FROM CLIENT"
        del self.players[name]

    def get_me(self):
        return self.me

    def set_my_character_condition(self, blurriness, redness):
        self.me.set_character_condition(blurriness, redness)