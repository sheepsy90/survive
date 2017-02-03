#!/usr/bin/env python
# -*- coding:utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
from server.configuration.configuration import Configuration
from server.xmlrpc_services.RequestHandler import RequestHandler
from server.xmlrpc_services.crafting.CraftingService import CraftingService


class CraftingServiceXMLRPC():

    def __init__(self, host, port):
        # Create server
        self.server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)
        self.server.register_introspection_functions()

        """ This is the service which handles the crafting recipes """

        item_service = CraftingService()
        self.server.register_instance(item_service)

    def start(self):
        # Run the server's main loop
        self.server.serve_forever()

if __name__ == '__main__':
    conf = Configuration()
    host, port = conf.configuration["CraftingXMLRPC"]

    print "[READING CONFIG FOR CraftingXMLRPC]", host, port

    cs = CraftingServiceXMLRPC(host, port)
    cs.start()