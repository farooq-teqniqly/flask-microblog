from app import app
from flask import render_template


@app.route("/")
@app.route("/index")
def index():
    params = dict(
        title="Welcome",
        user={"username": "farooqam"},
        posts=[
            dict(author={"username": "Bubba"}, body="Python is cool!"),
            dict(author={"username": "Felix"}, body="Mother's Day gift ideas?"),
        ],
    )

    return render_template("index.jinja2", **params)
