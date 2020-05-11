from uuid import uuid4

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config, EnvConfigFactory

app = Flask(__name__)

login = LoginManager(app)
login.login_view = "login"

config: Config = EnvConfigFactory.create()
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, errors


def get_id() -> str:
    return str(uuid4())


def seed_db(db):

    models.Post.query.delete()
    models.User.query.delete()
    db.session.commit()

    users = [
        models.User(
            id=get_id(),
            username="farooqam",
            email="farooqam@foo.com",
            about_me="I am cool!",
        ),
        models.User(
            id=get_id(),
            username="engreen",
            email="engreen@foo.com",
            about_me="I am principle based!",
        ),
    ]

    for user in users:
        user.set_password("1234")
        post = models.Post(
            id=get_id(), body=f"This is a post from {user.username}!", user_id=user.id
        )

        user.posts.append(post)

    db.session.add_all(users)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()


seed_db(db)
