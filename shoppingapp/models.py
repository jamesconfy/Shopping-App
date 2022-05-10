from flask_login import UserMixin
from shoppingapp import db, login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Producer.query.get(int(user_id))

class Consumer(UserMixin, db.Model):
    __tablename__ = 'consumer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(120), nullable=False)
    phoneNumber = db.Column(db.String(120), nullable=False, unique=True)
    dateCreated = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.username}\n {self.email}\n {self.phoneNumber}'

class Producer(UserMixin, db.Model):
    __tablename__ = 'producer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    office = db.Column(db.Text, nullable=False)
    phoneNumber = db.Column(db.String(120), nullable=False, unique=True)
    dateCreated = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    products = db.relationship('Product', backref='producer', lazy=True)

    def __repr__(self):
        return f'{self.username}\n {self.email}\n {self.phoneNumber}'

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    dateCreated = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('producer.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}\n {self.description}'