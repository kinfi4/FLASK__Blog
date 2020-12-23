# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template
from flask_login import current_user

from app import app, db
from app.models import Post


@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@app.route('/posts')
def posts():
    return render_template('posts.html', title='Home', posts=Post.query.all())


@app.route('/')
def main():
    title = 'Main Page'
    return render_template('base.html', title=title)


