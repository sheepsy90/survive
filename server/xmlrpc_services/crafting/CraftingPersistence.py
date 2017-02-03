# -*- coding:utf-8 -*-
import os
import sqlite3
import unittest
from common.ItemTemplate import ItemTemplate
from server.setup.ItemTemplateSetup import ItemTemplateSetup
from server.xmlrpc_services.crafting.CraftingRecipe import CraftingRecipe


class CraftingPersistenceSqlQueueCommand():

    CRAFTING_RECIPE_CREATION = 0
    ITEM_TYPE_CREATION = 1

    def __init__(self, type, data):
        self.type = type
        self.data = data


class CraftingPersistence():

    DUMMY_TYPE_NAME = "Dummy ItemTemplate"

    def __init__(self, database_name=""):
        if not os.path.isfile(database_name) or database_name == ":memory:":
            self.database_connection = sqlite3.connect(database_name)
            self.initialize_crafting_database()
        else:
            self.database_connection = sqlite3.connect(database_name)

    def initialize_crafting_database(self):
        cursor = self.database_connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS item_types
                                               (type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                path TEXT,
                                                level INTEGER,
                                                name TEXT,
                                                type_tags TEXT,
                                                initial_uses INTEGER,
                                                shape_x INTEGER,
                                                shape_y INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS crafting_recipes
                                               (crafting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                representation TEXT UNIQUE,
                                                forbidden BOOL,
                                                name TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS crafting_results
                                               (crafting_id INTEGER,
                                                type_id INTEGER,
                                                amount INTEGER,
                                                FOREIGN KEY(crafting_id) REFERENCES crafting_recipes(crafting_id)
                                                FOREIGN KEY(type_id) REFERENCES item_types(type_id))''')

        # Insert the initial item types

        item_type_setup = ItemTemplateSetup(cursor)
        item_type_setup.setup()

        self.save_crafting_recipe("18;18;19#18;18;19", False, "Electricl Component Assembly", [[20, 1]])

        self.database_connection.commit()

    def load_item_type_from_database(self, type_id):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT name, path, level, initial_uses, shape_x, shape_y, type_tags FROM item_types WHERE type_id = ?", [type_id])
        name, path, level, initial_use, shape_x, shape_y, type_tags = result.fetchone()

        return ItemTemplate(name, path, level, type_id, (shape_x, shape_y), initial_use, type_tags)

    def get_crafting_recipe(self, crafting_representation):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result1 = cursor.execute("SELECT crafting_id, name, forbidden FROM crafting_recipes WHERE representation = ?", [crafting_representation])
        value = result1.fetchone()

        if value is None:
            return None

        crafting_id, name, forbidden = value

        cr = CraftingRecipe(id, name, crafting_representation, forbidden)

        if not forbidden:
            result2 = cursor.execute("SELECT type_id, amount FROM crafting_results WHERE crafting_id = ?", [crafting_id])
            crafting_results = result2.fetchall()

            for e in crafting_results:
                cr.add_result(e)

        return cr

    def save_crafting_recipe(self, crafting_representation, forbidden, name, result):
        cursor = self.database_connection.cursor()

        cursor.execute("INSERT INTO crafting_recipes(representation, forbidden, name) VALUES (?, ?, ?)", [crafting_representation, forbidden, name])

        if not forbidden and len(result) > 0:
            crafting_id = cursor.lastrowid

            for element in result:
                type_id, amount = element
                cursor.execute("INSERT INTO crafting_results(crafting_id, type_id, amount) VALUES (?, ?, ?)", [crafting_id, type_id, amount])

        self.database_connection.commit()

    def get_maximum_item_type_id(self):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT max(type_id) FROM item_types")

        result = result.fetchone()

        if result[0] is None:
            return 0

        return result[0]

    def save_item_template(self, type_id, name, shape, initial_usages):
        cursor = self.database_connection.cursor()

        shape_x, shape_y = shape

        try:
            cursor.execute("INSERT INTO item_types(type_id, path, level, name, type_tags,  initial_uses, shape_x, shape_y) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [type_id, "/created/" + str(type_id), 0, name, ItemTemplate.EMPTY_TAGS_STRING, initial_usages, shape_x, shape_y])
            return True
        except:
            print "[ERROR] Tried to insert item_template as", type_id, name, shape, initial_usages
            return False

    def print_all_item_types(self):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT * FROM item_types")

        result = result.fetchall()

        for r in result:
            print r

    def get_item_types_by_drop_path_and_level(self, drop_path, level):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        stmt = "SELECT type_id, name, path, level, initial_uses, shape_x, shape_y, type_tags FROM item_types WHERE level = %i AND path LIKE '%s%%'" % (level, drop_path)
        print stmt
        result = cursor.execute(stmt)

        result = result.fetchall()
        complete_list = []

        if result is not None:
            for e in result:
                type_id, name, path, level, initial_use, shape_x, shape_y, type_tags = e
                it = ItemTemplate(name, path, level, type_id, (shape_x, shape_y), initial_use, type_tags)
                complete_list.append(it)
            return complete_list
        else:
            return complete_list

