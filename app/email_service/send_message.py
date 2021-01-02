from flask_mail import Message
from app import mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body

    mail.send(msg)
