from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config, EnvConfigFactory

app = Flask(__name__)

config: Config = EnvConfigFactory.create()
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
