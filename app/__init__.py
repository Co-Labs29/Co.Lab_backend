from flask import Flask
from config import Config
from flask_migrate import Migrate
from app.models import db, Parent
from .authentication.routes import auth
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)
CORS(app)

app.register_blueprint(auth)


migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)
db.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return Parent.query.get(int(user_id))


