# -*- coding:utf-8 -*-

from multiprocessing import Queue
import random
import threading
import unittest
import time
from server.xmlrpc_services.items.ItemPersistence import ItemPersistence


class ItemServiceSQLQueueCommand():

    DELETE_ITEM = 1
    CREATE_ITEM = 2
    UPDATE_ITEM_USAGE = 3

    def __init__(self, type, data):
        self.type = type
        self.data = data


class ItemService(threading.Thread):

    def __init__(self, db_path="items.db"):
        threading.Thread.__init__(self)

        self.db_path = db_path

        self.persistence = ItemPersistence(db_path)

        self.current_max_item_id = self.persistence.get_maximum_item_id()

        print "Startup compelte_ base id is", self.current_max_item_id
        self.item_id_lock = threading.Lock()

        self.item_creation_queue = Queue()

        self.start()

    def get_item_by_id(self, item_id):
        return self.persistence.get_item_by_id(item_id)

    def get_incremented_item_id(self):
        self.item_id_lock.acquire()
        self.current_max_item_id += 1
        value = self.current_max_item_id
        self.item_id_lock.release()
        return value

    def create_new_item(self, item_type_id, left_usages):
        new_id = self.get_incremented_item_id()
        self.item_creation_queue.put(ItemServiceSQLQueueCommand(
                                        ItemServiceSQLQueueCommand.CREATE_ITEM,
                                        [new_id, item_type_id, left_usages]))
        return new_id

    def delete_item(self, item_id):
        print "Shall Delete Item", item_id
        self.item_creation_queue.put(ItemServiceSQLQueueCommand(
                                        ItemServiceSQLQueueCommand.DELETE_ITEM,
                                        item_id))

    def update_item_usage(self, item_id, left_usages):
        self.item_creation_queue.put(ItemServiceSQLQueueCommand(
                                        ItemServiceSQLQueueCommand.UPDATE_ITEM_USAGE,
                                        [item_id, left_usages]))

    def run(self):
        persistence = ItemPersistence(self.db_path)

        while True:
            issqlqcomm = self.item_creation_queue.get()

            if issqlqcomm.type == ItemServiceSQLQueueCommand.CREATE_ITEM:
                new_id, item_type_id, left_usages = issqlqcomm.data
                persistence.create_item(new_id, item_type_id, left_usages)
            elif issqlqcomm.type == ItemServiceSQLQueueCommand.DELETE_ITEM:
                item_id = issqlqcomm.data
                persistence.delete_item(int(item_id))
            elif issqlqcomm.type == ItemServiceSQLQueueCommand.UPDATE_ITEM_USAGE:
                item_id, left_usages = issqlqcomm.data
                persistence.update_item_usage(item_id, left_usages)

            # Give other threads time to make things too
            time.sleep(0.05)