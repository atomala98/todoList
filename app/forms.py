from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime


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
    submit1 = SubmitField('Create task')


    def validate_deadline(form, field):
        print(field.data, datetime.now())
        if field.data < datetime.now():
            raise ValidationError('Deadline shouldn\'t be past.')  


class FilterForm(FlaskForm):
    sort_by = SelectField('Sort by', choices=['Date Created', 'Deadline'], validators=[])
    filter_by = SelectField('Filter by', choices=['All', 'Completed', "Uncompleted"], validators=[])
    submit2 = SubmitField('Filter')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    
class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[EqualTo("password")])
    submit = SubmitField('Reset password')
    
    
class TaskDescriptionForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit1 = SubmitField('Change description')
    
    
class SubtaskForm(FlaskForm):
    subtask = StringField('Subtask', validators=[DataRequired()])
    submit2 = SubmitField('Add subtask')
    
    
class CreateMessageForm(FlaskForm):
    receiver = StringField('Receiver', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send a message')
    
    
class MessageFilterForm(FlaskForm):
    sort_by = SelectField('Sort by', choices=['Newest', 'Oldest'], validators=[])
    filter_by = SelectField('Filter by', choices=['Received', 'Sent', "All"], validators=[])
    submit = SubmitField('Filter')