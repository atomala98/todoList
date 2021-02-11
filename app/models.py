from app import db, login, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time 

group_association_table = db.Table('association', db.Model.metadata,
    db.Column('left_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('group.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    messages = db.relationship('Message', backref='receiver', lazy='dynamic')
    authenticated = db.Column(db.Boolean, index=True, default=False)
    groups = db.relationship(
        'Group',
        secondary=group_association_table,
        back_populates="users")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_tasks(self):
        return Task.query.filter_by(user_id=self.id)
    
    def get_tasks_filtered(self, sort_by, filter_by):
        if filter_by == "All":
            tasks = Task.query.filter_by(user_id=self.id)
        elif filter_by == "Completed":
            tasks = Task.query.filter_by(user_id=self.id, is_completed=True)
        else:
            tasks = Task.query.filter_by(user_id=self.id, is_completed=False)
        if sort_by == "Date Created":
            return tasks.order_by(Task.timestamp)
        return tasks.order_by(Task.deadline)        
    
    def get_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    deadline = db.Column(db.DateTime, index=True)
    is_completed = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500), default="")
    subtasks = db.relationship('Subtask', backref='main_task', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Task {}>'.format(self.task)
    
    
class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140))
    is_completed = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    
    
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship(
        "User",
        secondary=group_association_table,
        back_populates="groups")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(40))
    text = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))