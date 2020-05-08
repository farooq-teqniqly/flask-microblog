from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
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
