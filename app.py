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


@app.route("/<id>")
def url_redirect_page(id):
    url_redirect_func = db_connection.DBConnection.url_redirect(id)
    original_url = url_redirect_func[1]
    if url_redirect_func:
        return redirect(original_url)
    else:
        flash("Invalid URL")
        return redirect(url_for("home"))


@app.route("/stats")
def stats():
    urls = db_connection.DBConnection.statistics()
    return render_template("stats.html", urls=urls)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=6000)
    app.run(host="0.0.0.0", port=8080, debug=True)
