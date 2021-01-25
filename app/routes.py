from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, TaskForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Task
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password")
            return redirect(url_for('index'))
        login_user(user)
        return redirect(url_for('menu'))
    return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is not None:
            flash("Username already taken!")
            return redirect(url_for('register'))
        if User.query.filter_by(email=form.email.data).first() is not None:
            flash("Email already registered!")
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    tasks = current_user.get_tasks()
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(task=form.task.data, deadline=form.deadline.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        tasks = current_user.get_tasks()
        return redirect('menu')
    return render_template('menu.html', user = current_user, form=form, tasks=tasks, date=datetime.now())

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    if Task.query.filter_by(id=int(id)).first():
        task = Task.query.filter_by(id=int(id)).first()
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('menu'))
    
@app.route('/change_status/<id>', methods=['GET', 'POST'])
def completed(id):
    if Task.query.filter_by(id=int(id)).first():
        task = Task.query.filter_by(id=int(id)).first()
        task.is_completed = not task.is_completed
        db.session.commit()
        return redirect(url_for('menu'))
    
    