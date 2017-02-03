# -*- coding:utf-8 -*-
from Queue import Queue
import threading
import time


class ItemListEntryLogger(threading.Thread):

    SEARCH_ITEM = 1
    CRAFT_ITEM = 2

    def __init__(self, log_file):
        threading.Thread.__init__(self)
        self.entry_queue = Queue()
        self.log_file = log_file

    def log_list_entry_for_player(self, player, position, entry):
        self.entry_queue.put([ItemListEntryLogger.SEARCH_ITEM, player, position, entry])

    def log_crafting_result(self, player, item_type_id, text):
        self.entry_queue.put([ItemListEntryLogger.CRAFT_ITEM, player, item_type_id, text])

    def run(self):
        while True:
            entry = self.entry_queue.get(block=True)
            with open(self.log_file, 'a') as f:
                if entry[0] == ItemListEntryLogger.SEARCH_ITEM:
                    f.write("[ItemListEntry][SEARCH] %s %s %s %s\n" % (str(time.time()), entry[1], entry[2], entry[3]))
                elif entry[0] == ItemListEntryLogger.CRAFT_ITEM:
                    f.write("[ItemListEntry][CRAFT] %s %s %s %s\n" % (str(time.time()), entry[1], entry[2], entry[3]))
