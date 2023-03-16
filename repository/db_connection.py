import config
from repository import db_connector
# import pyodbc
from flask import request
from hashids import Hashids
from config import SECRET_KEY


# Generating a hash using salt:
hashids = Hashids(min_length=4, salt=config.SECRET_KEY)


class DBConnection(object):
    connection = None

    @classmethod
    def get_connection(cls, new=False):
        """Creates return new Singleton database connection"""
        if new or not cls.connection:
            cls.connection = db_connector.DBConnector("database.db").create_connection()
        return cls.connection

    @classmethod
    def execute_query(cls, query):
        """execute query on singleton db connection"""
        connection = cls.get_connection()
        try:
            cursor = connection.cursor()
        except pyodbc.ProgrammingError:
            connection = cls.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        url_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        return result, url_id

    @classmethod
    def shorten_url(cls, url):
        """Commit original URL to database, then encode and create new short URL"""
        url_data = cls.execute_query(f"INSERT INTO urls (original_url) VALUES ('{url}')")
        url_id = url_data[1]

        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return short_url

    @classmethod
    def url_redirect(cls, id):
        """Decode URL, return original URL and add 1 to its clicks count"""
        original_id = hashids.decode(id)

        if original_id:
            original_id = original_id[0]
            url_data = cls.execute_query(f"SELECT original_url, clicks FROM urls WHERE id = ('{original_id}')")[0]

            original_url = url_data[0]["original_url"]
            clicks = url_data[0]["clicks"]

            cls.execute_query(f"UPDATE urls SET clicks = '{clicks + 1}' WHERE id = '{original_id}'")
            return True, original_url

    @classmethod
    def statistics(cls):
        """Select DB data, append to URL to visualize later in a HTML template"""
        db_urls = cls.execute_query("SELECT id, created, original_url, clicks FROM urls")[0]

        urls = []
        for url in db_urls:
            url = dict(url)
            url["short_url"] = request.host_url + hashids.encode(url["id"])
            urls.append(url)

        return urls