from flask import Blueprint
from flask_mail import Message

from . import mail
from .decorators import async_work

mails = Blueprint("mails", __name__)


def prepare_msg(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    return msg


@async_work
def send_async_email(subject, sender, recipients, text_body, html_body):
    msg = prepare_msg(subject, sender, recipients, text_body, html_body)
    mail.send(msg)


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = prepare_msg(subject, sender, recipients, text_body, html_body)
    mail.send(msg)
