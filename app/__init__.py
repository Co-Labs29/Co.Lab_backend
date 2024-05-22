from flask import Flask
from config import Config
from flask_migrate import Migrate
from app.models import db
from .authentication.routes import auth

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(auth)

db.init_app(app)
migrate = Migrate(app, db)