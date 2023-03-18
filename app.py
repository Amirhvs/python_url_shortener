from os import error
from flask import Flask, render_template, request, url_for, redirect, flash
from hashids import Hashids
import sqlite3
import uuid
import urllib.parse
import validators
import os

app = Flask(__name__)

# Needed for using Hashid. Could use UUID instead? Not super sure
app.config['SECRET_KEY'] = 'super_secret_string'
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

"""The get_db_connection() function opens a connection to the database.db database file 
and then sets the row_factory attribute to sqlite3.Row. As a result, 
you can have name-based access to columns; 
the database connection will return rows that behave like regular Python dictionaries.
Lastly, the function returns the conn connection object you’ll be using to access the database."""


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/url", methods=["POST"])
def add_url():
    url = request.json["url"]
    if not url:
        return "URL cannot be empty", 400

    is_valid = validators.url(url)
    if not is_valid:
        return "URL is not valid", 400

    conn = get_db_connection()

    url_data = conn.execute("INSERT INTO urls (original_url) VALUES (?)", (url,))
    conn.commit()
    conn.close()

    # handle errors
    server_url = os.getenv('SERVER_URL')

    url_id = url_data.lastrowid
    hashid = hashids.encode(url_id)
    short_url = f"{server_url}/{hashid}"

    # return render_template("index.html", short_url=short_url)
    return { "url": short_url }


    
    print(parsed_url)
    return {"works": True}

@app.route("/", methods=("GET", "POST"))
def home():
    # conn = get_db_connection()

    # if request.method == "POST":
    #     url = request.form["url"]
    #     # uid = str(uuid.uuid4())[:5]

    #     if not url:
    #         flash("The URL is required!")
    #         return redirect(url_for("index"))

    #     url_data = conn.execute("INSERT INTO urls (original_url) VALUES (?)", (url,))
    #     conn.commit()
    #     conn.close()

    #     url_id = url_data.lastrowid
    #     hashid = hashids.encode(url_id)
    #     short_url = request.host_url + hashid

    #     # return render_template("index.html", short_url=short_url)
    #     return { "url": short_url }

    return render_template("index.html")


@app.route("/<id>")
def url_redirect(id):
    conn = get_db_connection()

    original_id = hashids.decode(id)
    # print(original_id)
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute("SELECT original_url, clicks FROM urls"
                                " WHERE id = (?)", (original_id,)
                                ).fetchone()
        original_url = url_data["original_url"]
        clicks = url_data["clicks"]

        conn.execute("UPDATE urls SET clicks = ? WHERE id = ?",
                     (clicks+1, original_id))

        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash("Invalid URL")
        return redirect(url_for("home"))


@app.route("/stats")
def stats():
    conn = get_db_connection()
    db_urls = conn.execute("SELECT id, created, original_url, clicks FROM urls").fetchall()
    conn.close()

    urls = []
    for url in db_urls:
        url = dict(url)
        url["short_url"] = request.host_url + hashids.encode(url["id"])
        urls.append(url)

    return render_template("stats.html", urls=urls)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=6000)
    app.run(host="0.0.0.0", port=8080, debug=True)
