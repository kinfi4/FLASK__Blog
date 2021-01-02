from flask import flash, redirect, url_for, render_template
from flask_login import current_user

from app import app, db
from app.forms import EmailForResetPasswordForm, ResetPasswordForm
from app.models import User
from app.email_service.reset_password_message import send_password_email


@app.route('/reset_password_request', methods=['POST', 'GET'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('user_page', username=current_user.username))

    form = EmailForResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_email(user)

        flash('Check your email for the instructions to reset your password', category='info')
        return redirect(url_for('login'))

    return render_template('forms/password-reset-forms/email-for-reset-password-form.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('user_page', username=current_user.username))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('posts'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password_hash(form.password.data)
        db.session.commit()

        flash('Your password has been reset.', category='info')
        return redirect(url_for('login'))

    return render_template('forms/password-reset-forms/reset-password-form.html', form=form)
