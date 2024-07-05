from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    login = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='group', lazy='dynamic')
    
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    status = db.Column(db.String(64))
    price = db.Column(db.Float, default=1000)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    votes = db.relationship('Vote', backref='prompt', lazy='dynamic')
    notes = db.relationship('Note', backref='prompt', lazy='dynamic')
    
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_value = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'))
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_value = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'))