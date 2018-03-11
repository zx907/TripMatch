from datetime import datetime, timedelta

from flask import Blueprint, request, flash, render_template
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash


from flask import session as login_session

from ..db import Users, TripDetails, Destinations
from ..db import Session

manage = Blueprint('manage', __name__, url_prefix='/manage')


@manage.route('/', methods=['GET', 'POST'])
@manage.route('/manage_profile', methods=['GET', 'POST'])
def manage_profile():

    if request.method == 'POST':
        db_session = Session()
        try:
            user = db_session.query(Users).filter(Users.id == login_session['user_id']).first()
            user.email = request.form['NewEmail']
            user.password = generate_password_hash(request.form['NewPassword'])
            db_session.commit()
            flash('Profile updated successfully')
        except SQLAlchemyError:
            db_session.rollback()
            flash('Failed to update profile info')

    return render_template('manage_profile.html')


@manage.route('/manage_trips')
def manage_trips():
    session = Session()
    trips = session.query(TripDetails).filter(TripDetails.user_id == login_session['user_id']).all()
    return render_template('manage_trips.html', trips=trips)


@manage.context_processor
def utility_processor():
    def calc_date_end(start_date, duration):
        return (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(int(duration))).strftime('%Y-%m-%d')

    return dict(calc_date_end=calc_date_end)
