from datetime import datetime
from hashlib import md5

from . import db, login  # Use relative import
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __str__(self):
        return self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))
    image = db.Column(db.String(256))  # Assuming image paths are stored as strings
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __str__(self):
        return self.title


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"Conversation {self.id}"


class ConversationMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    conversation = db.relationship('Conversation', backref=db.backref('messages', lazy=True))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship('User')
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"


# User class remains the same


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(256))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)



