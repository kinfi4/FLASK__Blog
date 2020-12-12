# -*- coding: utf-8 -*- 
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post


@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', posts=Post.query.filter_by(user_id=current_user.id))


@app.route('/')
def main():
    title = 'Main Page'
    return render_template('base.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid password or login')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        # if user was sent to a login form, because he tried to get to the secured page
        # caused by decorator @login_required, and after singing in, he will be redirected
        # on the page he tried to enter
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', form=form, title='Sing in')


@app.route('/log-out')
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you successfully registered on MicroBlog!!')
        return redirect(url_for('index'))

    return render_template('register.html', title='Registration', form=form)

