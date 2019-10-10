from stck import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from stck import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    albums = db.relationship('Album', backref='albums', lazy='dynamic')

    def __repr__(self):
        return '<Artist {}>'.format(self.name)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    cds = db.Column(db.Integer, nullable=True)
    lps = db.Column(db.Integer, nullable=True)
    tapes = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Album {}>'.format(self.title)
