import xmlrpclib
from server.configuration.configuration import Configuration

__author__ = 'Infectiou'


class GameServerManagerClient(object):

    def __init__(self):
        config = Configuration()
        host, port = config.get_configuration()["GameServerManagerXMLRPC"]
        self.gameserver_manager = xmlrpclib.ServerProxy('http://%s:%s' % (str(host), str(port)), allow_none=True)

    def register_game_service(self, is_tutorial_area, area_to_serve, udp_ip, udp_port):
        self.gameserver_manager.register_game_service(is_tutorial_area, area_to_serve, udp_ip, udp_port)

    def get_game_service_for_area(self, tutorial_state,  area_of_player):
        return self.gameserver_manager.get_game_service_for_area(tutorial_state, area_of_player)

    def ping(self, is_tutorial_area, area_to_serve, udp_ip, udp_port):
        self.gameserver_manager.ping(is_tutorial_area, area_to_serve, udp_ip, udp_port)
