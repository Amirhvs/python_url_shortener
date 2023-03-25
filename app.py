from flask import Flask, render_template, request, url_for, redirect 
from repository import db_connection
from utils import get_hash_id 
import os
import validators
from sqlite3 import IntegrityError

app = Flask(__name__)
server_url = os.getenv("SERVER_URL")

@app.route("/url", methods=["POST"])
def add_url():
    
    """Validate URL, Commit original URL to database, then encode and create new short URL"""
    url = request.json["url"]
    if not url:
        return "URL cannot be empty", 400

    is_valid = validators.url(url)
    if not is_valid:
        return "URL is not valid", 400

    url_hash = get_hash_id()

    try:
        url_id = db_connection.DBConnection.insert_one(f"INSERT INTO urls (original_url, url_hash) VALUES ('{url}', '{url_hash}')")
        url_data = db_connection.DBConnection.fetch_one(f"SELECT * FROM urls WHERE id = {url_id}")

        return {"url": url_data["original_url"], "url_hash": url_data["url_hash"]}

    except IntegrityError:
        return "URL is already shortened", 400

@app.route("/url/<url_hash>", methods=['GET'])
def url_redirect_page(url_hash):
    res = db_connection.DBConnection.fetch_one(f"SELECT original_url FROM urls WHERE url_hash = '{url_hash}'")
    if res:
        original_url = res[0]
        return redirect(original_url) 
    else:
        return redirect(url_for("home"))


@app.route("/")
def home():
    """Select DB data, append to URL to visualize later in a HTML template"""
    db_urls = db_connection.DBConnection.execute_query_all("SELECT id, created, original_url, url_hash, clicks FROM urls")

    urls = []
    for url in db_urls:
        url = dict(url)
        urls.append(url)

    return render_template("stats.html", urls=urls)

if __name__ == "__main__":
    db_connection.DBConnection.run_migration() 
    app.run(host="0.0.0.0", port=8080, debug=True)
