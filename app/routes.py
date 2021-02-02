# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, g
from flask_login import current_user

from app import app, db
from app.forms import CreatePostForm, SearchForm


@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    g.search_form = SearchForm()


@app.route('/')
def main():
    title = 'Main Page'
    return render_template('base.html', title=title, form=CreatePostForm())


@app.route('/favicon.ico')
def favicon():
    return ''
