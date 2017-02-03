#!/usr/bin/env python
# -*- coding:utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import logging
from server.configuration.configuration import Configuration
from server.xmlrpc_services.RequestHandler import RequestHandler
from server.xmlrpc_services.gameservermanager.GameServerManager import GameServerManager


class SpecificHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write("<center>")
        self.wfile.write("<h4>Registered Clients</h4>")
        self.server.instance.tutorial_area_lock.acquire()
        for value in self.server.instance.registered_tutorial_areas.values():
            self.wfile.write(
                """<div style="border-radius: 5px; margin: 10px; border: 2px solid black;
                    padding: 5px; background-color: #ddd">GameServerArea - {}</div>""".format(str(value)))
        self.server.instance.tutorial_area_lock.release()

        for value in self.server.instance.registered_normal_areas.values():
            self.wfile.write(
                """<div style="border-radius: 5px; margin: 10px; border: 2px solid black;
                    padding: 5px; background-color: #ddd">GameServerArea - {}</div>""".format(str(value)))

        self.wfile.write("</center>")

if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] [%(name)s] %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='logs/game_server_manager.log',
                    level=logging.INFO)

    conf = Configuration()
    host, port = conf.configuration["GameServerManagerXMLRPC"]

    print "[READING CONFIG FOR GameServerManagerXMLRPC]", host, port

    # Create server
    server = SimpleXMLRPCServer((host, port), requestHandler=SpecificHandler, allow_none=True)
    server.register_introspection_functions()

    """ This service is like a registry where game_server_instances can register
        and can get infos where the other areas are served """


    game_server_manager = GameServerManager()
    server.register_instance(game_server_manager)

    # Run the server's main loop
    server.serve_forever()