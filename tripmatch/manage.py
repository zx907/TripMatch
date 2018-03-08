from flask import Blueprint, request, flash, render_template
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from db import Session
from model.tripmatch_model import Users, TripDetails
from flask import session as login_session

manage_page = Blueprint('manage', __name__, url_prefix='/manage')


@manage_page.route('/', methods=['GET', 'POST'])
@manage_page.route('/profile', methods=['GET', 'POST'])
def manage_profile():
    # if login_session.get('user_id', None):
    #     app.logger.info('login_session user_id: {}'.format(login_session['user_id']))
    #     return redirect(url_for('timeline'))

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

    return render_template('manage.manage_profile.html')


# @app.context_processor
@manage_page.route('/trips')
def manage_trips():
    session = Session()
    trips = session.query(TripDetails).filter(TripDetails.user_id == login_session['user_id']).all()
    app.logger.info(trips)
    return render_template('manage.manage_trips.html', trips=trips)
