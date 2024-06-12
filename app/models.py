from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta, timezone
import jwt
import pytz


db = SQLAlchemy()

class Parent(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String(10), nullable=False, default="parent")  # "parent or child"
    children = db.relationship('Child', backref='parent', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'email': self.email,
            'role': self.role
        }

    def get_jwt_token(self, secret_key):
        expiration = datetime.now(pytz.utc) + timedelta(weeks=1)
        payload = {
            'sub': self.id,
            'exp': expiration,
            'role': self.role
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token.decode('utf-8')

class Child(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String(10), nullable=False, default="child")
    img = db.Column(db.String, nullable=True) 
    chores = db.relationship('Chores', backref='child', lazy=True)
    wallet = db.relationship('Wallet', uselist=False, back_populates='child')
    goals = db.relationship('Goal', back_populates='child', lazy=True)
    img = db.Column(db.String, nullable=False, default="Avatar1.svg")

    def save(self):
        db.session.add(self)
        db.session.commit()


    def get_jwt_token(self, secret_key):
        expiration = datetime.now(pytz.utc) + timedelta(hours=1)
        payload = {
            'sub': self.id,
            'exp': expiration,
            'role': self.role
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token.decode('utf-8')



    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'username': self.username,
            'role': self.role,
            'img': self.img
        }
    

class Chores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("child.id"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("parent.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="not_completed")
    frequency = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Integer, nullable=False)

    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_child_username(self):
        return self.child.username

    def to_dict(self):
        return {
            "id": self.id,
            "child_id": self.child_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "status": self.status,
            "frequency": self.frequency,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "amount": self.amount
        } 

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    goal_account = db.Column(db.Float, nullable=False, default=0.0)
    child = db.relationship('Child', back_populates='wallet')
    goals = db.relationship('Goal', back_populates='wallet', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_amount(self, amount):
        self.amount += amount
        self.save()

    def sub_amount(self, amount):
        self.amount -= amount

    def get_balance(self):
        return self.amount
    
    def transfer_amount(self, amount):
        if self.amount >= amount:
            self.amount -= amount
            self.goal_account += amount
            self.save()
            return True
        return False

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Float, nullable=True, default=0)
    img = db.Column(db.String, nullable=True)
    link = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    complete = db.Column(db.Boolean, nullable=True, default=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    wallet = db.relationship('Wallet', back_populates='goals')
    child = db.relationship('Child', back_populates='goals')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_child_username(self):
        return self.child.username
  
    def to_dict(self):
        return {
            "id": self.id,
            "child_id": self.child_id,
            "name": self.name,
            "amount": self.amount,
            "paid": self.paid,
            "img": self.img,
            "link": self.link,
            "description": self.description,
            "complete": self.complete,
            "wallet_id": self.wallet_id
        }  
 

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("child.id"), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    child_username = db.Column(db.String, db.ForeignKey("child.username"), nullable=False)
    chores_id = db.Column(db.Integer, db.ForeignKey("chores.id"), nullable=True)
    goal_name = db.Column(db.String, nullable=True)
    chores_name = db.Column(db.String, nullable=True)
    chores_status = db.Column(db.String, nullable=True)
    goal_complete = db.Column(db.Boolean, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
