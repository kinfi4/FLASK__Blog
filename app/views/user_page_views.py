from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from wtforms import ValidationError

from app import app, db
from app.forms import EditProfileForm
from app.models import User, Post


@app.route('/user/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()

    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
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
        flash('This username is engaged', category='error')
        return redirect(url_for('edit_profile'))
