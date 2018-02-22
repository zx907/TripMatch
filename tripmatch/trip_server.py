from flask import Flask, g, app
from flask import blueprints
from flask import render_template, url_for, redirect, flash
from flask import session as login_session
from flask import make_response, Response, request
from flask import json, jsonify
from flask import abort
from flask_restful import Resource, Api, marshal
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import ClauseElement
from model.tripmatch_model import Base, Users, TripDetails, Waitinglist, Destinations
from werkzeug.security import check_password_hash, generate_password_hash, gen_salt
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
import random
import string
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('applogger')

PER_PAGE = 16
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tripmatch', 'static', 'user_uploaded_photos')
ALLOWED_EXTENSIONS = set(['bmp', 'jpeg', 'png'])
DEBUG = True

# configuration
APPLICATION_NAME = 'Trip Match'
app = Flask(__name__)
app.secret_key = ''.join(random.choice(
    string.ascii_uppercase + string.digits) for x in range(32))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# TRIPMATCH_SETTINGS = 'settings.txt'
# app.config.from_object(__name__)
# app.config.from_envvar('TRIPMATCH_SETTINGS', silent=True)

api = Api(app)

# database engine and session
engine = create_engine("sqlite:///" + os.getcwd() +
                       "/testdb.db", connect_args={'check_same_thread': False})
# create tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def timeline():
    logger.debug('timeline function')
    if login_session.get('user_id', None):
        login_status = True
    else:
        login_status = False
    logger.debug('login_status: {0}'.format(login_status))
    db_session = Session()
    trips = db_session.query(TripDetails).all()
    return render_template('timeline.html', trips=trips, login_status=login_status)


@app.route('/public')
def public_timeline():
    db_session = Session()
    trips = db_session.query(TripDetails).all()
    return render_template('timeline.html', trips=trips)


@app.route('/trip_detail/<int:trip_id>', methods=['GET', 'POST'])
def display_trip(trip_id):
    db_session = Session()
    if request.method == 'POST':
        if login_session.get('user_id', None) is None:
            return redirect(url_for('login'))
        text = request.form['message']
        user_id = login_session['user_id']
        trip_id = request.form['trip_id']
        post_date = datetime.now().isoformat(' ')

        db_session = Session()
        try:
            new_wtl_entry = Waitinglist(
                user_id=user_id, trip_id=trip_id, text=text, post_date=post_date)
            db_session.add(new_wtl_entry)
            db_session.commit()
        except:
            db_session.rollback()

    trip = db_session.query(TripDetails).filter_by(id=trip_id).one()
    waitinglist = db_session.query(
        Waitinglist).filter_by(trip_id=trip_id).all()
    return render_template('trip_details.html', trip=trip, waitinglist=waitinglist)


@app.route('/new_trip', methods=['GET', 'POST'])
def new_trip():
    app.logger.info('new_trip function')
    if 'user_id' not in login_session:
        redirect(url_for('login'))

    # post new trip
    if request.method == 'POST':

        db_session = Session()
        try:
            destination = get_or_create(
                db_session,
                Destinations,
                destination=request.form['destination']
            )[0]

            date_create = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

            new_trip = TripDetails(user_id=login_session['user_id'],
                                   destination_id=destination.id,
                                   duration=request.form['duration'],
                                   date_start=request.form['date_start'],
                                   companions=request.form['companions'],
                                   city_takeoff=request.form['city_takeoff'],
                                   expected_group_size=request.form['expected_group_size'],
                                   notes=request.form['notes'],
                                   date_create=date_create)

            # if no image is to upload, new_trip.ima_name = None
            if 'new_trip_img_file' not in request.files:
                app.logger.info('No file')

            file = request.files['new_trip_img_file']
            app.logger.info('original filename: {}'.format(file.filename))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_trip.img_name = filename
                app.logger.info('uploaded filename in new_trip: {}'.format(new_trip.img_name))
            else:
                new_trip.img_name = None
                app.logger.info('should be empty filename: {}'.format(new_trip.img_name))

            db_session.add(new_trip)
            db_session.commit()
            flash('Your trip is posted')
        # todo, specify what exception is expected here
        except Exception as e:
            db_session.rollback()
            app.logger.info(e)
            flash('Failed to post your trip')

    return render_template('new_trip.html')


# Reuse same template as new_trip, but prefill forms with existing infomation
@app.route('/edit_trip/<int:trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    app.logger.info('edit_trip function')
    if 'user_id' not in login_session:
        redirect(url_for('login'))


    # post new trip
    if request.method == 'POST':

        db_session = Session()
        try:
            destination = get_or_create(
                db_session,
                Destinations,
                destination=request.form['destination']
            )[0]

            date_create = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

            new_trip = TripDetails(user_id=login_session['user_id'],
                                   destination_id=destination.id,
                                   duration=request.form['duration'],
                                   date_start=request.form['date_start'],
                                   companions=request.form['companions'],
                                   city_takeoff=request.form['city_takeoff'],
                                   expected_group_size=request.form['expected_group_size'],
                                   notes=request.form['notes'],
                                   date_create=date_create)

            # if no image is to upload, new_trip.ima_name = None
            if 'new_trip_img_file' not in request.files:
                app.logger.info('No file')

            file = request.files['new_trip_img_file']
            app.logger.info('original filename: {}'.format(file.filename))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_trip.img_name = filename
                app.logger.info('uploaded filename in new_trip: {}'.format(new_trip.img_name))
            else:
                new_trip.img_name = None
                app.logger.info('should be empty filename: {}'.format(new_trip.img_name))

            db_session.add(new_trip)
            db_session.commit()
            flash('Your trip is posted')
        # todo, specify what exception is expected here
        except Exception as e:
            db_session.rollback()
            app.logger.info(e)
            flash('Failed to post your trip')

    return render_template('new_trip.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Log user in and save logged-in username in login_session dict

    # redirect to home page if user has already been logged in
    if login_session.get('user_id', None):
        app.logger.info(login_session['user_id'])
        return redirect(url_for('timeline'))
    error = None
    # Log user in
    if request.method == 'POST':
        db_session = Session()
        user = db_session.query(Users).filter(
            Users.username == request.form['username']).first()
        if user is None:
            error = 'invalid username'
            flash('invalid username')
        elif not check_password_hash(user.password, request.form['password']):
            error = 'invalid password'
            flash('invalid password')
        # Add a cookie to response obj
        # elif request.form.get('remember_me', None) :
        #     print('set cookie')
        #     resp = make_response(redirect(url_for('timeline')))
        #     resp.set_cookie('tripmatch_user_id', str(user.id))
        #     login_session['user_id'] = user.id
        #     return resp
        else:
            flash('you were logged in')
            login_session['user_id'] = user.id
            return redirect(url_for('timeline'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    login_session.pop('user_id')
    # if request.cookie.get('user_id', None):
    #     resp = make_response(redirect(url_for('public_timeline')))
    #     resp.set_cookie('tripmatch_user_id', user.id, 0)
    #     flash('You were logged out')
    #     print('logout successful')
    #     return resp
    # else:
    flash('You were logged out')
    return redirect(url_for('timeline'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if login_session.get('user_id', None) is not None:
        return redirect(url_for('timeline'))
    error = None

    # Todo: hashtable replace if-else

    if request.method == 'POST':
        if not request.form['username']:
            error = 'Please enter a username'
        elif username_exists(request.form['username']):
            error = 'The username is already taken'
        elif not request.form['email']:
            error = 'Please enter an email address'
        elif email_exists(request.form['email']):
            error = 'The email address is already taken'
        elif not request.form['password']:
            error = 'Please enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'Passwords are not matched'
        else:
            db_session = Session()
            try:
                new_user = Users(
                    username=request.form['username'], email=request.form['email'],
                    password=generate_password_hash(request.form['password']))
                db_session.add(new_user)
                db_session.commit()
                flash('Register successfully')
                return redirect(url_for('timeline'))
            except:
                db_session.rollback()
                flash('Registion failure')
                return redirect(url_for('timeline'))

    return render_template('register.html')


def email_exists(email):
    db_session = Session()
    return db_session.query(Users).filter(Users.email == email).first()


def username_exists(username):
    db_session = sessionmaker()()
    return db_session.query(Users).filter(Users.username == username).first()


def item_exists(session, model, item):
    '''
    query database with session and model to check if a specific item already exists in database
    :return: item or None
    '''
    instance = session.query(model).filter_by(item).first()
    return instance


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items()
                      if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True


def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_trip_img', methods=['GET', 'POST'])
def upload_trip_img():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded file', filename=filename))


@app.route('/manage', methods=['GET', 'POST'])
@app.route('/manage/profile', methods=['GET', 'POST'])
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

    return render_template('manage_profile.html')


# @app.context_processor
@app.route('/manage/trips')
def manage_trips():
    session = Session()
    trips = session.query(TripDetails).filter(TripDetails.user_id == login_session['user_id']).all()
    app.logger.info(trips)
    return render_template('manage_trips.html', trips=trips)


@app.route('/manage/inbox')
def manage_inbox():
    session = Session()
    messages = session.query(Messages).join(Users).filter(Users.id == login_session['user_id']).all()
    return render_template('manage_inbox.html', messages=messages)


@app.context_processor
def utility_processor():
    def calc_date_end(start_date, duration):
        return (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(int(duration))).strftime('%Y-%m-%d')
    return dict(calc_date_end=calc_date_end)

# Restful api
class UserAPI(Resource):
    def get(self, user_id):
        db_session = Session()
        user = db_session.query(Users).filter_by(id=user_id).one()
        return jsonify(user.to_dict())

    def put(self, user_id):
        db_session = Session()
        user = db_session.query(Users).filter_by(id=user_id).one()
        return jsonify(user.to_dict())

    def delete(self, user_id):
        db_session = Session()
        user = db_session.query(Users).filter_by(id=user_id).one()
        if not user:
            db_session.delete(user)


class TripAPI(Resource):
    def get(self, trip_id):
        db_session = Session()
        trip = db_session.query(TripDetails).filter_by(id=trip_id).one()
        return jsonify(trip.to_dict())

    def put(self, trip_id):
        db_session = Session()
        trip = db_session.query(TripDetails).filter_by(id=trip_id).one()
        return jsonify(trip.to_dict())

    def delete(self, trip_id):
        db_session = Session()
        trip = db_session.query(TripDetails).filter_by(id=trip_id).one()
        if not trip:
            db_session.delete(trip)


class DestinationAPI(Resource):
    def get(self, destination_id):
        db_session = Session()
        destination = db_session.query(TripDetails).filter_by(id=destination_id).one()
        return jsonify(destination.to_dict())

    def put(self, destination_id):
        db_session = Session()
        destination = db_session.query(TripDetails).filter_by(id=destination_id).one()
        return jsonify(destination.to_dict())

    def delete(self, destination_id):
        db_session = Session()
        destination = db_session.query(TripDetails).filter_by(id=destination_id).one()
        if not destination:
            db_session.delete(destination)


api.add_resource(UserAPI, '/user_api/<int:user_id>')
api.add_resource(TripAPI, '/trip_api/<int:trip_id>')
api.add_resource(DestinationAPI, '/destination_api/<int:destination_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
