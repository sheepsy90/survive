class OnlinePlayerSystem(object):

    def __init__(self):
        self.online_players = {}
        self.connection_to_player = {}

        self.moving_players = {}

    def add_online_player(self, player):
        self.online_players[player.get_id()] = player
        self.connection_to_player[player.get_connection()] = player

    def get_player_on_connection(self, conn):
        assert conn in self.connection_to_player.keys()
        return self.connection_to_player[conn]

    def get_player_on_id(self, id):
        print self.online_players
        assert id in self.online_players.keys()
        return self.online_players[id]

    def remove_player(self, player):
        del self.online_players[player.get_id()]
        del self.connection_to_player[player.get_connection()]

    def register_moving_player(self, player):
        """ This method registers a player to the list of currently moving players which then handles the movement """
        self.moving_players[player.get_id()] = player

    def remove_moving_player(self, player_id):
        del self.moving_players[player_id]

