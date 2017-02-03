#!/usr/bin/env python
# -*- coding:utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from server.configuration.configuration import Configuration
from server.xmlrpc_services.RequestHandler import RequestHandler
from server.xmlrpc_services.player.PlayerHandlerService import PlayerHandlerService


if __name__ == '__main__':

    conf = Configuration()
    host, port = conf.configuration["PlayerHandlerServiceXMLRPC"]

    print "[READING CONFIG FOR PlayerHandlerServiceXMLRPC]", host, port

    # Create server
    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)
    server.register_introspection_functions()

    """ This service only handles on which areas a player may login and changes that when servers issues commands for that """
    """ -> Note the positions of players are 'in service' persistenced only if ther is an area change """

    player_handler = PlayerHandlerService()
    server.register_instance(player_handler)

    # Run the server's main loop
    server.serve_forever()
