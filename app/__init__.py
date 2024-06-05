from flask import Flask
from config import Config
from flask_migrate import Migrate
from app.models import db, Parent
from .authentication.routes import auth
from flask_cors import CORS
from .site.routes import site
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
app.config['JWT_ACCESS_TOKENT_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

app.config.from_object(Config)
CORS(app)

app.register_blueprint(auth)
app.register_blueprint(site)


db.init_app(app)
migrate = Migrate(app, db)


