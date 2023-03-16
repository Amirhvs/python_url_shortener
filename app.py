from flask import Flask, render_template, request, url_for, redirect, flash
from repository import db_connection, db_connector

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route("/", methods=("GET", "POST"))
def home():

    if request.method == "POST":
        url = request.form["url"]

        if not url:
            flash("The URL is required!")
            return redirect(url_for("index"))

        short_url = db_connection.DBConnection.shorten_url(url)

        return render_template("index.html", short_url=short_url)

    return render_template("index.html")


# @app.route("/<id>")
# def url_redirect(id):
#     conn = get_db_connection()
#
#     original_id = hashids.decode(id)
#     # print(original_id)
#     if original_id:
#         original_id = original_id[0]
#         url_data = conn.execute("SELECT original_url, clicks FROM urls"
#                                 " WHERE id = (?)", (original_id,)
#                                 ).fetchone()
#         original_url = url_data["original_url"]
#         clicks = url_data["clicks"]
#
#         conn.execute("UPDATE urls SET clicks = ? WHERE id = ?",
#                      (clicks+1, original_id))
#
#         conn.commit()
#         conn.close()
#         return redirect(original_url)
#     else:
#         flash("Invalid URL")
#         return redirect(url_for("home"))
#
#
# @app.route("/stats")
# def stats():
#     conn = get_db_connection()
#     db_urls = conn.execute("SELECT id, created, original_url, clicks FROM urls").fetchall()
#     conn.close()
#
#     urls = []
#     for url in db_urls:
#         url = dict(url)
#         url["short_url"] = request.host_url + hashids.encode(url["id"])
#         urls.append(url)
#
#     return render_template("stats.html", urls=urls)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=6000)
    app.run(host="0.0.0.0", port=8080, debug=True)
