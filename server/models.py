from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    recipes = db.relationship('Recipe', backref='user', lazy=True)

    @property
    def password_hash(self):
        raise AttributeError('password_hash is not readable.')

    @password_hash.setter
    def password_hash(self, password):
        if password:
            self._password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def authenticate(self, password):
        return self.verify_password(password)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required.")
        return username

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long.")
        return instructions

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title is required.")
        return title
