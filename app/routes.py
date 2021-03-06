from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import SubtaskForm, LoginForm, RegisterForm, TaskForm, FilterForm, ResetPasswordForm, ChangePasswordForm, TaskDescriptionForm, CreateMessageForm, MessageFilterForm, CreateGroupForm, GroupInvititionsForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Task, Subtask, Group, Message
from datetime import datetime
from app.mails import send_password_reset_email, send_auth_email

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password.")
            return redirect(url_for('index'))
        if not user.authenticated:
            flash("Activate your account.")
            return redirect(url_for('index'))
        login_user(user)
        return redirect(url_for('menu'))
    return render_template('index.html', form=form)

@login_required
@app.route('/user/<id>')
def user(id):
    user = User.query.filter_by(id=id).first()
    return render_template('user.html', user=user)

@login_required
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
        if User.query.filter_by(username=form.username.data, authenticated=False).first() is not None:
            User.query.filter_by(username=form.username.data, authenticated=False).delete()
            db.session.commit()
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
        send_auth_email(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@login_required
@app.route('/groups')
def groups():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    groups = current_user.groups
    return render_template('groups.html', groups=groups)

@login_required
@app.route('/group/<id>', methods=['GET', 'POST'])
def group(id):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    group = Group.query.filter_by(id=id).first()
    if not group:
        flash("Group does not exist.")
        return redirect(url_for('groups'))
    if current_user not in group.users:
        flash("You are not in this group.")
        return redirect(url_for('menu'))
    form = GroupInvititionsForm()
    task_form = TaskForm()
    tasks = group.tasks
    if form.submit.data and form.validate_on_submit():
        receiver = User.query.filter_by(username=form.name.data).first()
        if receiver and receiver not in group.users:
            text = render_template("invitation/msg.html", group=group, sender=current_user, receiver=receiver)
            message = Message(sender=current_user, text=text, receiver=receiver)        
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('group', id=id))
        elif not receiver:
            flash(("User {} does not exist.").format(form.name.data))
        else:
            flash(("User {} already in group.").format(form.name.data))
    if task_form.submit1.data and task_form.validate_on_submit():
        task = Task(task=task_form.task.data, deadline=task_form.deadline.data, group=group)
        db.session.add(task)
        db.session.commit()
        tasks = group.tasks
        return redirect(url_for('group', id=id))
    return render_template('group.html', form=form, group=group, tasks=tasks, task_form=task_form)


@login_required
@app.route('/group_invite/<group_id>/<user_id>')
def group_invite(group_id, user_id):
    group = Group.query.filter_by(id=group_id).first()
    if not group:
        flash(('Group does not exist.'))
        return redirect(url_for('groups'))
    if current_user.id != group.admin_id:
        flash(('You are not admin of group.'))
        return redirect(url_for('groups'))
    group.add_user(User.query.filter_by(id=user_id).first())
    db.session.commit()
    return redirect(url_for('group', id=group_id))


@login_required
@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateGroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data, admin_id=current_user.id)
        group.add_user(current_user)
        db.session.commit()
        return redirect(url_for('groups'))
    return render_template('create_group.html', form=form)


@login_required
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = MessageFilterForm()
    msg = current_user.get_messages()
    if form.validate_on_submit():
        msg = current_user.get_messages_filtered(form.sort_by.data, form.filter_by.data)
    return render_template('messages.html', form=form, messages=msg)


@login_required
@app.route('/create_message', methods=['GET', 'POST'])
def create_message():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateMessageForm()
    if form.validate_on_submit():
        receiver = User.query.filter_by(username=form.receiver.data).first()
        if receiver:
            text = form.message.data.replace('\n', '<br>')
            message = Message(sender=current_user, text=text, receiver=User.query.filter_by(username=form.receiver.data).first())
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('messages'))
        else:
            flash(("User {} does not exist.").format(form.receiver.data))
    return render_template('create_message.html', form=form)

@login_required
@app.route('/delete_message/<id>', methods=['GET', 'POST'])
def delete_message(id):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    message = Message.query.filter_by(id=id).first()
    if message.receiver_id != current_user.id:
        return redirect(url_for('menu'))
    if message:
        msg = Message.query.filter_by(id=id).first()
        db.session.delete(msg)
        db.session.commit()
        return redirect(url_for('messages'))


@login_required
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    task_form = TaskForm()
    filter_form = FilterForm()
    tasks = current_user.get_tasks()
    if task_form.submit1.data and task_form.validate_on_submit():
        task = Task(task=task_form.task.data, deadline=task_form.deadline.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        tasks = current_user.get_tasks()
        return redirect(url_for('menu'))
    if filter_form.submit2.data and filter_form.validate_on_submit():
        tasks = current_user.get_tasks_filtered(filter_form.sort_by.data, filter_form.filter_by.data)
    return render_template('menu.html', user=current_user, form=task_form, filter_form=filter_form, tasks=tasks, date=datetime.now())


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('index'))
    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    user = User.verify_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('reset_password.html', form=form)


@app.route('/auth/<token>')
def auth(token):
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    user = User.verify_token(token)
    user.authenticated = True
    db.session.commit()
    return redirect(url_for('index'))


@login_required
@app.route('/task/<id>', methods=['GET', 'POST'])
def task(id):
    if not current_user.is_authenticated:
        return redirect(url_for('menu'))
    description_form = TaskDescriptionForm()
    task = Task.query.filter_by(id=int(id)).first()
    sub_form = SubtaskForm()
    if description_form.submit1.data and description_form.validate_on_submit():
        task.description = description_form.description.data
        db.session.commit()
        if task.group:
            return redirect(url_for('group', id=task.group.id))
        return redirect(url_for('menu'))
    if sub_form.submit2.data and sub_form.validate_on_submit():
        if len(task.subtasks.all()) < 5:
            subtask = Subtask(task=sub_form.subtask.data, main_task=task)
            db.session.add(task)
            db.session.commit()
        else:
            flash("More than 5 subtasks!")
    return render_template('task.html', task=task, form=description_form, sub_form=sub_form)


@login_required
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    if not current_user.is_authenticated:
        return redirect(url_for('menu'))
    task = Task.query.filter_by(id=int(id)).first()    
    if not task:
        flash("No task in database.")
        return redirect(url_for('menu'))
    if task.user_id:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for('menu'))
        else:
            flash("No permission to delete this task.")
    elif task.group_id:
        group = task.group
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('group', id=group.id))
    return redirect(url_for('menu'))


@login_required
@app.route('/change_status/<id>', methods=['GET', 'POST'])
def completed(id):
    if not current_user.is_authenticated:
        return redirect(url_for('menu'))
    task = Task.query.filter_by(id=int(id)).first()    
    if not task:
        flash("No task in database.")
        return redirect(url_for('menu'))
    if task.user_id:
        if task.user_id == current_user.id:
            task.is_completed = not task.is_completed
            db.session.commit()
            return redirect(url_for('menu'))
        else:
            flash("No permission to change this task status.")
    elif task.group_id:
        group = task.group
        task.is_completed = not task.is_completed
        db.session.commit()
        return redirect(url_for('group', id=group.id))
    return redirect(url_for('menu'))


@app.route('/delete/<id>/<sub_id>', methods=['GET', 'POST'])
def delete_sub(id, sub_id):
    if not current_user.is_authenticated:
        return redirect(url_for('menu'))
    subtask = Subtask.query.filter_by(id=int(sub_id)).first()
    if subtask and subtask.main_task.user_id == current_user.id:
        db.session.delete(subtask)
        db.session.commit()
        return redirect(url_for('task', id=id))
    elif subtask.main_task.user_id != current_user.id:
        flash("You have no permission to change this task status.")
        return redirect(url_for('menu'))
    else:
        flash ("No subtask to delete.")
    return redirect(url_for('task', id=id))


@app.route('/change_status/<id>/<sub_id>', methods=['GET', 'POST'])
def completed_sub(id, sub_id):
    if not current_user.is_authenticated:
        return redirect(url_for('menu'))
    subtask = Subtask.query.filter_by(id=int(sub_id)).first()
    if subtask and subtask.main_task.user_id == current_user.id:
        subtask.is_completed = not subtask.is_completed
        db.session.commit()
        return redirect(url_for('task', id=id))
    elif subtask.main_task.user_id != current_user.id:
        flash("You have no permission to change this task status.")
        return redirect(url_for('menu'))
    else:
        flash("No subtask to change status")
    return redirect(url_for('task', id=id))


@app.route('/group_delete/<id>', methods=['GET', 'POST'])
def group_delete(id):
    if not current_user.is_authenticated:
        return redirect(url_for('menu'))
    if Group.query.filter_by(id=id).first():
        group = Group.query.filter_by(id=id).first()
        if group.admin_id == current_user.id:
            db.session.delete(group)
            db.session.commit()
            return redirect(url_for('groups'))
        else:
            flash("You are not group owner!")
    return redirect(url_for('menu'))

@app.route('/delete_from_group/<id>/<group_id>', methods=['GET', 'POST'])
def delete_from_group(id, group_id):
    if not current_user.is_authenticated:
        return redirect(url_for('menu'))
    if Group.query.filter_by(id=group_id).first() and User.query.filter_by(id=id).first():
        user = User.query.filter_by(id=id).first()
        group = Group.query.filter_by(id=group_id).first()
        if group.admin_id == current_user.id and user in group.users:
            group.remove_user(user)
            db.session.commit()
            return redirect(url_for('group', id=group_id))
        elif group.admin_id != current_user.id:
            flash("You have no permissions to delete user from group!")
        else:
            flash("No user in group")
    return redirect(url_for('menu'))