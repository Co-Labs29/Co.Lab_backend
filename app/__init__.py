from flask import Flask
from config import Config
from flask_migrate import Migrate
from app.models import db
from .authentication.routes import auth
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)
CORS(app)

app.register_blueprint(auth)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)