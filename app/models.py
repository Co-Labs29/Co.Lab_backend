# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import uuid 
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from flask_login import LoginManager
# from flask_marshmallow import Marshmallow 
# import secrets

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Parent(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.String(10), nullable=False, default="parent") # "parent or child"
    children = db.relationship('Child', backref='parent', lazy=True)

    def __init__(self, first_name, email, password, role):
        self.first_name = first_name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def save(self):
        db.session.add(self)
        db.session.commit()

class Child(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    username = db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.String(10), nullable=False, default="child") # "parent or child"
    chores = db.relationship('Chores', backref='child', lazy=True)

    def __init__(self, parent_id, username, password, role):
        self.parent_id = parent_id
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def save(self):
        db.session.add(self)
        db.session.commit()

class Chores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("child.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    frequency = db.Column(db.String, nullable=False)

    def __init__(self, child_id, name, is_completed, frequency):
        self.child_id = child_id
        self.name = name
        self.is_completed = is_completed
        self.frequency = frequency

    def save(self):
        db.session.add(self)
        db.session.commit()







