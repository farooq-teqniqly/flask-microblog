import uuid

from werkzeug.urls import url_parse

from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms.loginform import LoginForm
from app.forms.userregform import UserRegistrationForm
from app.models import User, Post


@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = Post.query.all()
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("/index"))

    form = UserRegistrationForm()

    if form.validate_on_submit():
        user = User(
            id=str(uuid.uuid4()), username=form.username.data, email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)

        try:
            db.session.commit()
            flash("Registration successful!")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            flash(e)
        finally:
            db.session.close()

    params = dict(title="Register", form=form)
    return render_template("userreg.jinja2", **params)


@app.route("/user/<username>")
def user(username: str):
    user = User.query.filter_by(username=username).first_or_404()

    posts = [
        {"author": user, "body": "Beautiful day in Seattle!"},
        {"author": user, "body": "Bombshell movie was so cool!"},
    ]

    return render_template("user.jinja2", user=user, posts=posts)
