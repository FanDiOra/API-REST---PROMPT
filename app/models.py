from app import db

class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user', name='user_role'), nullable=False)
    groupID = db.Column(db.Integer, db.ForeignKey('group.groupID'))

class Group(db.Model):
    __tablename__ = 'group'
    groupID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    users = db.relationship('User', backref='group', lazy='dynamic')

class Prompt(db.Model):
    __tablename__ = 'prompt'
    promptID = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, default=1000)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    edit_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    votes = db.relationship('Vote', backref='prompt', lazy='dynamic')
    notes = db.relationship('Note', backref='prompt', lazy='dynamic')

class Vote(db.Model):
    __tablename__ = 'vote'
    voteID = db.Column(db.Integer, primary_key=True)
    vote_value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.promptID'))

class Note(db.Model):
    __tablename__ = 'note'
    noteID = db.Column(db.Integer, primary_key=True)
    note_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.promptID'))
