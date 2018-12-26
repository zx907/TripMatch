from .. import celery
from flask_mail import Message, Mail

from flask import Blueprint

mail = Blueprint('mail', __name__, url_prefix='/mail')
mail_app = Mail(mail)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail_app.send(msg)


@celery.task()
def send_registration_confirm_mail(recipient):
    send_email("New Registration From Tripmatch", "no_reply@tripmatch.com", recipient,
               "Thank your for register our community, hope you can find trip pal here.")
