import os
import unittest
import sqlite3
from server.xmlrpc_services.login.Account import Account


class AccountPersistence():

    def __init__(self, database_name=""):
        if not os.path.isfile(database_name):
            self.database_connection = sqlite3.connect(database_name)
            self.initialize_crafting_database()
        else:
            self.database_connection = sqlite3.connect(database_name)

    def initialize_crafting_database(self):
        cursor = self.database_connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
                                               (account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                username TEXT UNIQUE,
                                                password TEXT,
                                                session_key TEXT)''')

        # Insert Start Backpack Size
        cursor.execute("INSERT INTO accounts(username, password) VALUES (?, ?)", ["sheepy", "sheepy"])
        cursor.execute("INSERT INTO accounts(username, password) VALUES (?, ?)", ["alex", "alex"])
        cursor.execute("INSERT INTO accounts(username, password) VALUES (?, ?)", ["malte", "malte"])

        self.database_connection.commit()

    def create_account(self, username, password):
        cursor = self.database_connection.cursor()
        cursor.execute("INSERT INTO accounts(username, password) VALUES (?, ?)", [username, password])

    def load_account_by_name(self, username):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT account_id, password, session_key FROM accounts WHERE username = ?", [username])
        fetched_result = result.fetchone()

        if fetched_result is not None:
            account_id, password, session_key = fetched_result
            return Account(account_id, username, password, session_key)

    def load_account_by_id(self, account_id):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT username, password, session_key FROM accounts WHERE account_id = ?", [account_id])
        fetched_result = result.fetchone()

        if fetched_result is not None:
            username, password, session_key = fetched_result
            return Account(account_id, username, password, session_key)

    def set_session_key_for_account(self, account_id, session_key):
        cursor = self.database_connection.cursor()

        cursor.execute("UPDATE accounts SET session_key = ? WHERE account_id = ?", [session_key, account_id])

        self.database_connection.commit()

    def has_username(self, username):
        cursor = self.database_connection.cursor()

        # Insert a row of data
        result = cursor.execute("SELECT account_id FROM accounts WHERE username = ?", [username])
        fetched_result = result.fetchone()

        return fetched_result is not None


class AccountPersistenceTest(unittest.TestCase):

    def test_account_persistence_plain_works(self):
        ap = AccountPersistence(":memory:")

        account = ap.load_account_by_name("sheepy")
        self.assertIsNotNone(account)

        self.assertTrue(ap.has_username("sheepy"))
        self.assertFalse(ap.has_username("sheepy_none"))
