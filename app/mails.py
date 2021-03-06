from flask_mail import Message
from flask import render_template
from app import mail, app

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    
    
def send_password_reset_email(user):
    token = user.get_token()
    send_email('Reset Your Password at todoList',
                sender=app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
                html_body=render_template('email/reset_password.html',
                                        user=user, token=token))
    
    
def send_auth_email(user):
    token = user.get_token()
    print('x')
    send_email('Authenticate your account',
                sender=app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('auth/auth.txt',
                                        user=user, token=token),
                html_body=render_template('auth/auth.html',
                                        user=user, token=token))