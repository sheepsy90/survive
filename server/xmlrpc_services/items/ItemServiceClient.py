# -*- coding:utf-8 -*-
"""

^^^^^^^^^^^^

.. moduleauthor:: sheepy <sheepy@informatik.uni-hamburg.de>

History:
* 14.11.14: Created (sheepy)

"""
import xmlrpclib

from server.configuration.configuration import Configuration
from server.xmlrpc_services.items.Item import Item


class ItemServiceClient(object):

    def __init__(self):
        config = Configuration()
        host, port = config.get_configuration()["ItemPersistenceServiceXMLRPC"]
        self.player_service = xmlrpclib.ServerProxy('http://%s:%s' % (str(host), str(port)), allow_none=True)

    def __create_new_item(self, item_type_id, left_usages):
        return self.player_service.create_new_item(item_type_id, left_usages)

    def __delete_item(self, item_id):
        return self.player_service.delete_item(item_id)

    def __update_item_usage(self, item_id, left_usages):
        return self.player_service.update_item_usage(item_id, left_usages)

    def create_multiple_items(self, item_template, amount):

        type_id = item_template.type_id
        initial_uses = item_template.initial_uses

        items = []
        for i in range(amount):
            item_id = self.__create_new_item(type_id, initial_uses)
            items.append(Item(item_template, item_id, initial_uses))

        return items

    def get_item(self, item_id):
        return self.player_service.get_item_by_id(item_id)

    def delete_item(self, item_id):
        print "DELETE", item_id
        self.player_service.delete_item(item_id)