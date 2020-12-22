# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, CreatePostForm
from app.models import User, Post


@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/posts')
def posts():
    return render_template('posts.html', title='Home', posts=Post.query.all())


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you successfully registered on MicroBlog!!', category='info')
        return redirect(url_for('posts'))

    return render_template('forms/register.html', title='Registration', form=form)


@app.route('/user/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()

    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your changes have been saved.', category='info')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.name.data = current_user.username
        form.about_me.data = current_user.about_me
        return render_template('forms/edit-profile.html', form=form)
    else:
        flash('Ops, something gone wrong', category='error')
        return redirect(url_for('main'))


@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm()

    if request.method == 'POST':
        post = Post()

        if form.validate_on_submit():
            post.user_id = current_user.id
            post.body = form.body.data

            db.session.add(post)
            db.session.commit()

        return redirect(url_for('user_page', username=current_user.username))

    else:
        context = {
            'form': form,
            'title': 'Create post'
        }

        return render_template('forms/create-post.html', **context)


@app.route('/delete_post/<id_>', methods=['POST'])
@login_required
def delete_post(id_):
    post = Post.query.filter_by(user_id=current_user.id).filter_by(id=id_).first()
    if not post:
        abort(405)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_page', username=current_user.username))
