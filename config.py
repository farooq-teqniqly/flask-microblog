import os
from typing import Any, Dict

from dotenv import load_dotenv


class Config(object):
    def __init__(
        self,
        secret_key: str,
        sqlalchemy_database_uri: str,
        sqlalchemy_track_modifications: bool,
    ):
        self.SECRET_KEY = secret_key
        self.SQLALCHEMY_DATABASE_URI = sqlalchemy_database_uri
        self.SQLALCHEMY_TRACK_MODIFICATIONS = sqlalchemy_track_modifications


class EnvConfigFactory:
    @staticmethod
    def create() -> Config:
        load_dotenv()
        secret_key = os.getenv("SECRET_KEY")
        db_uri = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db', 'app.db')}"
        db_track_modifications = False

        if not secret_key:
            raise ValueError("SECRET_KEY must be set!")

        return Config(secret_key, db_uri, db_track_modifications)
