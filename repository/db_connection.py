from repository import db_connector

class DBConnection(object):
    connection = None

    @classmethod
    def get_connection(cls, new=False):
        """Creates return new Singleton database connection"""
        if new or not cls.connection:
            cls.connection = db_connector.DBConnector("data/database.db").create_connection()
        return cls.connection

    @classmethod
    def execute_query_all(cls, query):
        """execute query on singleton db connection"""
        connection = cls.get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()

        cursor.close()
        return result

    @classmethod
    def insert_one(cls, query):
        """execute query on singleton db connection"""
        connection = cls.get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        result = cursor.lastrowid

        cursor.close()
        return result

    @classmethod
    def fetch_one(cls, query):
        """execute query on singleton db connection"""
        connection = cls.get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        return result

    @classmethod
    def run_migration(cls):
        connection = cls.get_connection() 
        with open('./schema.sql') as f:
            connection.executescript(f.read())
            connection.commit()
