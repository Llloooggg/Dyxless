from flask import Blueprint
from flask_mail import Message

from . import app, mail
from .decorators import async_work

mails = Blueprint("mails", __name__)


def prepare_msg(subject, recipients, body, html, sender):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    msg.html = html
    return msg


@async_work
def send_async_email(
    subject,
    recipients,
    body=None,
    html=None,
    sender=app.config["APP_EMAIL"],
):
    msg = prepare_msg(subject, recipients, body, html, sender)
    with app.app_context():
        mail.send(msg)


def send_mail(
    subject,
    recipients,
    body=None,
    html=None,
    sender=app.config["APP_EMAIL"],
):
    msg = prepare_msg(subject, recipients, body, html, sender)
    mail.send(msg)
