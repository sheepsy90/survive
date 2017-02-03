#!/usr/bin/env python
# -*- coding:utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from server.configuration.configuration import Configuration
from server.xmlrpc_services.RequestHandler import RequestHandler
from server.xmlrpc_services.item_list_entry_logger.ItemListEntryLogger import ItemListEntryLogger

if __name__ == '__main__':

    conf = Configuration()
    host, port = conf.configuration["ItemListEntryLoggerXMLRPC"]

    print "[READING CONFIG FOR ItemListEntryLoggerXMLRPC]", host, port

    # Create server
    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)
    server.register_introspection_functions()

    item_list_entry_logger = ItemListEntryLogger('sample_list')
    item_list_entry_logger.start()
    server.register_instance(item_list_entry_logger)

    # Run the server's main loop
    server.serve_forever()