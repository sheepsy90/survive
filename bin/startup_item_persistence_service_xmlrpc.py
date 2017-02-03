#!/usr/bin/env python
# -*- coding:utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from server.configuration.configuration import Configuration
from server.xmlrpc_services.RequestHandler import RequestHandler
from server.xmlrpc_services.items.ItemService import ItemService

if __name__ == '__main__':

    conf = Configuration()
    host, port = conf.configuration["ItemPersistenceServiceXMLRPC"]

    print "[READING CONFIG FOR ItemPersistenceServiceXMLRPC]", host, port
    # Create server
    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)
    server.register_introspection_functions()

    item_service = ItemService()
    server.register_instance(item_service)

    # Run the server's main loop
    server.serve_forever()