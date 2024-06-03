from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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

class Child(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String(10), nullable=False, default="child")  # "parent or child"
    chores = db.relationship('Chores', backref='child', lazy=True)
    wallet = db.relationship('Wallet', uselist=False, back_populates='child')
    goals = db.relationship('Goal', back_populates='child', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'username': self.username,
            'role': self.role
        }
    

class Chores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("child.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    frequency = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

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
    img = db.Column(db.String, nullable=True)
    link = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    wallet = db.relationship('Wallet', back_populates='goals')
    child = db.relationship('Child', back_populates='goals')

    def save(self):
        db.session.add(self)
        db.session.commit()
