from flask import flash, redirect, url_for
from flask_login import current_user

from app import db, app
from app.models import User


@app.route('/follow/<username>')
def follow(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash(f'User {user.username} doesnt exist', category='error')
        return redirect(url_for('main'))

    if user == current_user:
        flash(f'U cant subscribe on yourself', category='error')
        return redirect(url_for('user_page', username=current_user.username))

    current_user.follow(user)
    db.session.commit()
    flash(f'You are following {username}')
    return redirect(url_for('user_page', username=username))


@app.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash(f'User {user.username} doesnt exist', category='error')
        return redirect(url_for('main'))

    if user == current_user:
        flash(f'U cant unsubscribe from yourself', category='error')
        return redirect(url_for('user_page', username=current_user.username))

    current_user.unfollow(user)
    db.session.commit()
    flash(f'You unfollow {username}')
    return redirect(url_for('user_page', username=username))

