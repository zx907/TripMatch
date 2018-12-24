from datetime import datetime, timedelta

from flask import Blueprint, request, flash, render_template, g
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from flask import session as login_session

from ..utils import login_required
from ..db import Users, TripDetails, Destinations

from flask_mail import Message
from flask_mail import Mail

from ..message_queue import make_celery

manage = Blueprint('manage', __name__, url_prefix='/manage')
celery = make_celery(manage)

mail = Mail()
mail.init_app(manage)

@manage.route('/', methods=['GET', 'POST'])
@manage.route('/manage_profile', methods=['GET', 'POST'])
@login_required
def manage_profile():

    if request.method == 'POST':
        try:
            user = g.db_session.query(Users).filter(Users.id == login_session['user_id']).first()
            user.email = request.form['NewEmail']
            user.password = generate_password_hash(request.form['NewPassword'])
            g.db_session.commit()
            flash('Profile updated successfully')
        except SQLAlchemyError:
            g.db_session.rollback()
            flash('Failed to update profile info')

    return render_template('manage_profile.html')


@manage.route('/manage_trips')
@login_required
def manage_trips():
    trips = g.db_session.query(TripDetails).filter(TripDetails.user_id == login_session['user_id']).all()
    return render_template('manage_trips.html', trips=trips)


@manage.context_processor
def utility_processor():
    def calc_date_end(start_date, duration):
        if not isinstance(duration, int):
            duration = 1
        return (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(int(duration))).strftime('%Y-%m-%d')

    return dict(calc_date_end=calc_date_end)


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)


@celery.task()
def send_registration_confirm_mail(recipient):
    send_email("New Registration From Tripmatch", "no_reply@tripmatch.com", recipient,
               "Thank your for register our community, hope you can find trip pal here.")
