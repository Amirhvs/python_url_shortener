import sqlite3

class DBConnector(object):

    def __init__(self, driver, server, database, user, password):
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.dbconn = None

    # creats new connection
    def create_connection(self):
        return sqlite3.connect("/data/database.db")

    # For explicitly opening database connection
    def __enter__(self):
        self.dbconn = self.create_connection()
        return self.dbconn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dbconn.close()
