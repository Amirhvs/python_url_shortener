import sqlite3

class DBConnector(object):

    def __init__(self, db_path):
        self.db_path = db_path

    # creates new connection
    def create_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    # For explicitly opening database connection
    def __enter__(self):
        self.dbconn = self.create_connection()

    def __exit__(self ):
        self.dbconn.close()
