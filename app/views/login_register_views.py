# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid password or login', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        # if user was sent to a login form, because he tried to get to the secured page
        # caused by decorator @login_required, and after singing in, he will be redirected
        # on the page he tried to enter
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('posts')

        return redirect(next_page)

    return render_template('forms/login.html', form=form, title='Sing in')


@app.route('/log-out')
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, full_name=form.full_name.data)
        user.set_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you successfully registered on MicroBlog!!', category='info')
        return redirect(url_for('posts'))

    return render_template('forms/register.html', title='Registration', form=form)



