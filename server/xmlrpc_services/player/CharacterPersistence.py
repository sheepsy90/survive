# -*- coding:utf-8 -*-
import os
import sqlite3
import unittest


class CharacterPersistence():

    def __init__(self, database_name='players.db'):
        self.INITIAL_AREA = 6

        if not os.path.isfile(database_name):
            self.database_connection = sqlite3.connect(database_name)
            self.initialize_player_database()
        else:
            self.database_connection = sqlite3.connect(database_name)

    def create_character(self, account_id, character_name):
        cursor = self.database_connection.cursor()


        # Insert a row of data
        cursor.execute("INSERT INTO "
                       "players(account_id, character_name, pos_x, pos_y, orientation, area_id, tutorial_state) "
                       "VALUES ('%(account_id)i',"
                       "        '%(character_name)s',"
                       "        '%(pos_x)i', "
                       "        '%(pos_y)i', "
                       "        '%(orientation)i', "
                       "        '%(area_id)i', "
                       "        '%(tutorial_state)i')" % {
            "account_id": account_id,
            "character_name": character_name,
            "pos_x": 15,
            "pos_y": 39,
            "orientation": 1,
            "area_id": self.INITIAL_AREA,
            "tutorial_state": 0})

        character_id = cursor.lastrowid

        # Insert Start Backpack Size
        cursor.execute("INSERT INTO backpack_sizes(character_id, size_x, size_y) VALUES (?, ?, ?)", [character_id, 12, 5])

        cursor.execute("INSERT INTO wearings(character_id, items_id_list) VALUES (?, ?)", [character_id, ""])

        self.database_connection.commit()

        return character_id, self.INITIAL_AREA

    def initialize_player_database(self):
        cursor = self.database_connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS players
                                               (character_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                account_id INTEGER,
                                                character_name TEXT,
                                                pos_x INTEGER,
                                                pos_y INTEGER,
                                                orientation INTEGER,
                                                area_id INTEGER,
                                                tutorial_state INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS backpack_sizes
                                               (character_id INTEGER PRIMARY KEY,
                                                size_x INTEGER,
                                                size_y INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS backpack_content
                                               (character_id INTEGER,
                                                item_id INTEGER,
                                                start_pos_x INTEGER,
                                                start_pos_y INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS wearings
                                               (character_id INTEGER,
                                                items_id_list TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS character_health_modifiers
                                               (character_id INTEGER,
                                                health_modifier_type_id INTEGER,
                                                health_modifier_amount INTEGER)''')

        self.database_connection.commit()

    def get_available_characters_for_account(self, account_id):
        cursor = self.database_connection.cursor()

        cursor.execute("SELECT character_id, character_name FROM players WHERE account_id = '%i'" % account_id)

        return cursor.fetchall()

    def get_character_area(self, account_id, character_id):
        cursor = self.database_connection.cursor()

        cursor.execute("SELECT area_id FROM players WHERE account_id = '%i' AND character_id = '%i'" % (account_id, character_id))

        result = cursor.fetchone()

        if result is None:
            return None
        else:
            return result[0]

    def can_create_character(self, account_id):
        cursor = self.database_connection.cursor()

        cursor.execute("SELECT * FROM players WHERE account_id = ?", [account_id])

        result = cursor.fetchall()

        return len(result) < 4

    def get_character(self, character_id):
        cursor = self.database_connection.cursor()

        cursor.execute("SELECT * FROM players WHERE character_id = ?", [character_id])

        result = cursor.fetchone()

        if result is None:
            return None

        data = {
           "character_id": result[0],
           "account_id": result[1],
           "character_name": result[2],
           "pos_x": result[3],
           "pos_y": result[4],
           "orientation": result[5],
           "area_id": result[6],
           "tutorial_state": result[7]
        }
        print data

        return data

    def set_character_to_new_area(self, account_id, character_id, new_area_id, start_position):
        cursor = self.database_connection.cursor()

        orientation, pos_x, pos_y = start_position

        cursor.execute("UPDATE players "
                       "SET pos_x = ?, pos_y = ?, orientation = ?, area_id = ? "
                       "WHERE account_id = ? AND character_id = ?",
                       [pos_x, pos_y, orientation, new_area_id, account_id, character_id])

        self.database_connection.commit()

    def save_player_position(self, account_id, character_id, discrete_position):
        cursor = self.database_connection.cursor()

        orientation, pos_x, pos_y = discrete_position

        cursor.execute("UPDATE players "
                       "SET pos_x = ?, pos_y = ?, orientation = ? "
                       "WHERE account_id = ? AND character_id = ?",
                       [pos_x, pos_y, orientation, account_id, character_id])

        print "Saved position", pos_x, pos_y, orientation

        self.database_connection.commit()

    def get_backpack_size_for_character(self, character_id):
        cursor = self.database_connection.cursor()

        cursor.execute("SELECT size_x, size_y FROM backpack_sizes WHERE character_id = '%i'" % character_id)

        return cursor.fetchone()

    def get_backpack_items_for_character(self, character_id):
        cursor = self.database_connection.cursor()

        cursor.execute("SELECT item_id, start_pos_x, start_pos_y FROM backpack_content WHERE character_id = '%i'" % character_id)

        return cursor.fetchall()

    def save_backpack_items(self, character_id, prepared_info):

        cursor = self.database_connection.cursor()

        cursor.execute("DELETE FROM backpack_content WHERE character_id = '%i'" % character_id)
        for key in prepared_info:
            sx, sy = prepared_info[key]
            cursor.execute("INSERT INTO backpack_content(character_id, item_id, start_pos_x, start_pos_y) VALUES (?, ?, ?, ?)", [character_id, int(key), sx, sy])
            print "Saved item", key, sx, sy, character_id
        self.database_connection.commit()

    def get_player_health_modifiers(self, character_id):
        cursor = self.database_connection.cursor()

        cursor.execute("SELECT health_modifier_type_id, health_modifier_amount FROM character_health_modifiers WHERE character_id = ?", [character_id])

        return cursor.fetchall()

    def save_health_modifiers(self, character_id, modifiers):
        cursor = self.database_connection.cursor()

        cursor.execute("DELETE FROM character_health_modifiers WHERE character_id = '%i'" % character_id)
        for mod in modifiers:
            type, amount = mod
            cursor.execute("INSERT INTO character_health_modifiers(character_id, health_modifier_type_id, health_modifier_amount) VALUES (?, ?, ?)", [character_id, type, amount])
            print "Saved health_mod", character_id, type, amount

        self.database_connection.commit()

    def save_wearing_states(self, character_id, wearing_states):
        cursor = self.database_connection.cursor()

        list_as_string = str(wearing_states)
        list_as_string = list_as_string[1:]
        list_as_string = list_as_string[:-1]
        list_as_string = list_as_string.replace(" ", "")

        cursor.execute("UPDATE wearings SET items_id_list = ? WHERE character_id = ? ", [list_as_string, character_id])

        self.database_connection.commit()

    def get_wearing_states(self, character_id):
        cursor = self.database_connection.cursor()

        cursor.execute("SELECT items_id_list FROM wearings WHERE character_id = ? ", [character_id])
        result = cursor.fetchone()

        if result is None:
            return []

        if len(result) != 1:
            return None

        try:
            result = result[0]
            splitted = result.split(",")
            wearing_list = [int(e) for e in splitted if len(e) > 0]
            self.database_connection.commit()
            return wearing_list
        except:
            return None

    def save_tutorial_state(self, character_id, tutorial_state):
        cursor = self.database_connection.cursor()

        cursor.execute("UPDATE players SET tutorial_state = ? WHERE character_id = ? ", [tutorial_state, character_id])

        self.database_connection.commit()
