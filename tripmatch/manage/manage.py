from datetime import datetime, timedelta

from flask import Blueprint, request, flash, render_template, g
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash


from flask import session as login_session

from ..utils import login_required
from ..db import Users, TripDetails, Destinations

manage = Blueprint('manage', __name__, url_prefix='/manage')


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
        return (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(int(duration))).strftime('%Y-%m-%d')

    return dict(calc_date_end=calc_date_end)
