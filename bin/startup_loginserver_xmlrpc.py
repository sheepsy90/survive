#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

from SimpleXMLRPCServer import SimpleXMLRPCServer
from server.configuration.configuration import Configuration
from server.xmlrpc_services.RequestHandler import RequestHandler
from server.xmlrpc_services.login.LoginServerHandler import LoginServerHandler


if __name__ == '__main__':

    logging.basicConfig(format='[%(levelname)s] [%(name)s] %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='logs/login_server.log',
                    level=logging.INFO)

    conf = Configuration()
    host, port = conf.configuration["LoginServerHandlerXMLRPC"]

    print "[READING CONFIG FOR LoginServerHandlerXMLRPC]", host, port

    # Create server
    server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True)

    """ This service is available from the outside and is the first point of interaction with the game server system for
        login and connection info retrieval """

    login_server_handler = LoginServerHandler()
    server.register_instance(login_server_handler)

    # Run the server's main loop
    server.serve_forever()
