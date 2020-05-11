from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    about_me = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(256))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        d = dict(
            id=self.id,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
        )

        return f"<User> {d}"
        return f"<User> {d}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_gravatar(self, size=80):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()

        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Post(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    body = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        d = dict(
            id=self.id,
            user_id=self.user_id,
            body=len(self.body),
            timestamp=self.timestamp,
        )

        return f"<Post> {d}"


@login.user_loader
def load_user(user_id: str):
    return User.query.get(user_id)
