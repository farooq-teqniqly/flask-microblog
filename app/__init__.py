from flask import Flask
from config import Config, EnvConfigFactory

app = Flask(__name__)

config: Config = EnvConfigFactory.create()
app.config.from_object(config)

from app import routes
