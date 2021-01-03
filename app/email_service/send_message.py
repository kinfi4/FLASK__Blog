from flask_mail import Message
from app import mail, app
from threading import Thread


def send_message_async(application, msg):
    with application.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body

    Thread(target=send_message_async, args=(app, msg)).start()
