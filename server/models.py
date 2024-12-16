from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    _password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(500), nullable=True, default=None)
    bio = db.Column(db.Text, nullable=True, default=None)

    recipes = db.relationship("Recipe", backref="owner", lazy="dynamic")

    @property
    def password_hash(self):
        raise AttributeError("Password is not directly accessible.")
    
    @password_hash.setter
    def password_hash(self, password):
        """Sets password_hash."""
        if not password:
            raise ValueError("Password is required.")
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks the password against the hashed version."""
        return bcrypt.check_password_hash(self._password_hash, password)

    def authenticate(self, password):
        """Authenticates the user with the password."""
        return self.check_password(password)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required.")
        
        if User.query.filter_by(username=username).first():
            raise IntegrityError("Username already exists.")
        return username

    @validates('password_hash')
    def validate_password(self, key, password):
        if not password:
            raise ValueError("Password is required.")
        return password

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='owned_recipes') 

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

    @validates('user_id')
    def validate_user_id(self, key, user_id):
        """Validate that user_id is not None or invalid."""
        if not user_id:
            raise ValueError("User ID is required for recipe.")
        user = User.query.get(user_id)
        if user is None:
            raise ValueError(f"No user found with ID {user_id}.")
        return user_id

    __table_args__ = (
        CheckConstraint('length(instructions) >= 50', name='check_instructions_length'),
    )
