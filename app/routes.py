# -*- coding: utf-8 -*- 
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/')
def main():
    title = 'Main Page'
    return render_template('base.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Thank you for your singing in, {form.login.data} and {form.password.data} you are welcome')
        return redirect('/index')

    return render_template('login.html', form=form, title='Sign in')
