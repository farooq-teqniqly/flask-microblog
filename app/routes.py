from app import app
from flask import render_template, flash, redirect, url_for
from app.forms.loginform import LoginForm


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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(
            f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}"
        )
        return redirect(url_for("index"))

    params = dict(title="Sign In", form=form)
    return render_template("login.jinja2", **params)
