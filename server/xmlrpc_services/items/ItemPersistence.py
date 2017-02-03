# -*- coding:utf-8 -*-
"""

^^^^^^^^^^^^

.. moduleauthor:: sheepy <sheepy@informatik.uni-hamburg.de>

History:
* 14.11.14: Created (sheepy)

"""
import SimpleXMLRPCServer
import SocketServer
import os
import sqlite3
import unittest


class ItemPersistence(object):

    def __init__(self, database_name='items.db'):
        self.INITIAL_AREA = 1

        if not os.path.isfile(database_name):
            self.database_connection = sqlite3.connect(database_name)
            self.initialize_items_database()
        else:
            self.database_connection = sqlite3.connect(database_name)

    def create_item(self, item_id, type_id, usages_left):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        cursor.execute("INSERT INTO "
                       "items(item_id, item_type, usages_left) "
                       "VALUES ('%(item_id)i',"
                       "        '%(item_type)i',"
                       "        '%(usages_left)i')" % {
            "item_id": item_id,
            "item_type": type_id,
            "usages_left": usages_left})

        self.database_connection.commit()

    def initialize_items_database(self):
        cursor = self.database_connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS items
                                               (item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                item_type INTEGER,
                                                usages_left INTEGER)''')

        self.database_connection.commit()


    def get_maximum_item_id(self):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT max(item_id) FROM items")

        result = result.fetchone()

        if result[0] is None:
            return 0

        return result[0]


    def get_all(self):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT * FROM items")

        return result.fetchall()

    def get_item_by_id(self, item_id):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT * FROM items WHERE item_id = ?", [item_id])

        return result.fetchone()

    def delete_item(self, item_id):
        cursor = self.database_connection.cursor()
        # Insert a row of data
        cursor.execute("DELETE FROM items WHERE item_id = ?", [item_id])

    def update_item_usage(self, item_id, left_usages):
        cursor = self.database_connection.cursor()
        # Insert a row of data
        cursor.execute("UPDATE items "
                       "SET usages_left = ? "
                       "WHERE item_id = ? ",
                       [left_usages, item_id])