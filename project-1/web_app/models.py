from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default = func.now())
    photos = db.relationship('Photo', backref='user', lazy=True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'))
    created_at = db.Column(db.DateTime(timezone=True), default = func.now())

    def __init__(self, filename, filepath, user_id):
        self.filename = filename
        self.filepath = filepath
        self.user_id = user_id