import os
import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            print("✅ Conexión a la base de datos establecida.")

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("✅ Conexión a la base de datos cerrada.")

    def execute_query(self, query, params=()):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()