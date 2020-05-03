import os
from dotenv import load_dotenv


class Config(object):
    def __init__(self, secret_key: str):
        self.SECRET_KEY = secret_key


class EnvConfigFactory:
    @staticmethod
    def create() -> Config:
        load_dotenv()
        secret_key = os.getenv("SECRET_KEY")

        if not secret_key:
            raise ValueError("SECRET_KEY must be set!")

        return Config(secret_key)
