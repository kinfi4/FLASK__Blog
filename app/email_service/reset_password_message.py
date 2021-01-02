from app.email_service.send_message import send_email
from flask import render_template
from app import app


def send_password_email(user):
    token = user.get_reset_password_token()
    send_email('[KinfiBook] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email_templates/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email_templates/reset_password.html',
                                         user=user, token=token))

