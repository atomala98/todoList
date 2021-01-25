from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateTimeLocalField

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[EqualTo("password")])
    submit = SubmitField('Register')
    
class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    deadline = DateTimeLocalField('Deadline', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Create task')