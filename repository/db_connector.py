import sqlite3

class DBConnector(object):

    def __init__(self, database):
        self.database = database

    # creates new connection
    def create_connection(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        return conn

    # For explicitly opening database connection
    def __enter__(self):
        self.dbconn = self.create_connection()
        return self.dbconn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dbconn.close()
