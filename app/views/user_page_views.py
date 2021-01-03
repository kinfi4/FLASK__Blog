from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from wtforms import ValidationError

from app import app, db
from app.forms import EditProfileForm
from app.models import User, Post


@app.route('/user/<username>')
def user_page(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)

    posts_for_page = Post.query.filter_by(user_id=user.id).order_by(Post.timespan.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    next_page = url_for('user_page', username=username,
                        page=posts_for_page.next_num) if posts_for_page.has_next else None
    prev_page = url_for('user_page', username=username,
                        page=posts_for_page.prev_num) if posts_for_page.has_prev else None

    return render_template('user.html', user=user, posts=posts_for_page.items, next_page=next_page, prev_page=prev_page)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        current_user.full_name = form.full_name.data

        db.session.commit()

        flash('Your changes have been saved.', category='info')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.name.data = current_user.username
        form.about_me.data = current_user.about_me
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        return render_template('forms/edit-profile.html', form=form)
    else:
        flash(form, category='error')
        return redirect(url_for('edit_profile'))
