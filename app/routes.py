from werkzeug.urls import url_parse

from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms.loginform import LoginForm
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = [
        {"author": {"username": "farooqam"}, "body": "Beautiful day in Seattle!"},
        {"author": {"username": "engreen"}, "body": "Bombshell movie was so cool!"},
    ]

    params = dict(title="Welcome", posts=posts)

    return render_template("index.jinja2", **params)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("/index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user or not user.check_password(form.password.data):
            flash("Invalid username and/or password.")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")

        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)

    params = dict(title="Sign In", form=form)
    return render_template("login.jinja2", **params)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
