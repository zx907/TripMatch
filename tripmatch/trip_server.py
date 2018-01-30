from flask import Flask, g, app
from flask import render_template, url_for, redirect, flash
from flask import session as login_session
from flask import make_response, Response, request
from flask import json, jsonify
from flask import abort
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import ClauseElement
from model.tripmatch_model import Base, Users, TripDetails, Waitinglist, Destinations
from werkzeug.security import check_password_hash, generate_password_hash, gen_salt
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
import requests
import random
import string
import os
import logging


PER_PAGE = 16
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tripmatch', 'user_uploaded_photos')
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
def init_db():
    Base.metadata.create_all(engine)


def get_db_session():
    return sessionmaker(bind=engine)()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def timeline():
    db_session = get_db_session()
    trips = db_session.query(TripDetails).all()
    return render_template('timeline.html', trips=trips)


@app.route('/public')
def public_timeline():
    db_session = get_db_session()
    trips = db_session.query(TripDetails).all()
    return render_template('timeline.html', trips=trips)


@app.route('/trip_detail/<int:trip_id>', methods=['GET', 'POST'])
def display_trip(trip_id):
    db_session = get_db_session()
    if request.method == 'POST':
        if login_session.get('user_id', None) == None:
            return redirect(url_for('login'))
        text = request.form['message']
        user_id = login_session['user_id']
        trip_id = request.form['trip_id']
        post_date = datetime.now().isoformat(' ')

        db_session = get_db_session()
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
    if 'user_id' not in login_session:
        redirect(url_for('login'))

    if request.method == 'POST':

        db_session = get_db_session()
        try:
            destination = get_or_create(
                db_session,
                Destinations,
                destination=request.form['destination']
            )[0]

            date_create = datetime.now().isoformat(' ')

            new_trip = TripDetails(user_id=login_session['user_id'],
                                   destination_id=destination.id,
                                   duration=request.form['duration'],
                                   date_start=request.form['date_start'],
                                   companions=request.form['companions'],
                                   city_takeoff=request.form['city_takeoff'],
                                   expected_group_size=request.form['expected_group_size'],
                                   notes=request.form['notes'],
                                   date_create=date_create)

            # if 'file' not in request.files:
            #     flash('No file part')

            file = request.files['file']
            # print(file)
            # if file.filename=='':
            #     flash('No selected file')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_trip.img_name = filename
                print('3')

            db_session.add(new_trip)
            db_session.commit()
            flash('Your trip is posted')
        except Exception as e:
            db_session.rollback()
            print(e)
            flash('Failed to post your trip')

    return render_template('new_trip.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Log user in and save logged-in username in login_session dict
    if login_session.get('user_id', None):
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        db_session = get_db_session()
        user = db_session.query(Users).filter(
            Users.username == request.form['username']).first()
        if user == None:
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
    del login_session['user_id']
    if request.cookie.get('user_id', None):
        resp = make_response(redirect(url_for('public_timeline')))
        resp.set_cookie('tripmatch_user_id', user.id, 0)
        flash('You were logged out')
        print('logout successful')
        return resp
    else:
        flash('You were logged out')
        print('logout successful')
        return redirect(url_for('public_timeline'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if login_session.get('user_id', None) != None:
        return redirect(url_for('timeline'))
    error = None

    #Todo: hashtable replace if-else

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
            db_session = get_db_session()
            try:
                new_user = Users(
                    username=request.form['username'], email=request.form['email'], password=generate_password_hash(request.form['password']))
                db_session.add(new_user)
                db_session.commit()
                flash('Register successfully')
                return redirect(url_for('timeline'))
            except:
                db_session.rollback()
                flash('Registion failed')
                return redirect(url_for('timeline'))

    return render_template('register.html')


def email_exists(email):
    db_session = get_db_session()
    return db_session.query(Users).filter(Users.email == email).first()


def username_exists(username):
    db_session = get_db_session()
    return db_session.query(Users).filter(Users.username == username).first()


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

# Restful api part
class UserAPI(Resource):
    def get(self, user_id) :
        user = db_session.query(Users).filter_by(id=user_id).one()
        return user

    def put(self, user_id):
        user = db_session.query(Users).filter_by(id=user_id).one()
        return user

    def delete(self, user_id):
        user = db_session.query(Users).filter_by(id=user_id).one()
        if not user:
            session.delete(user)

class TripAPI(Resource):
    def get(self, trip_id) :
        trip = db_session.query(TripsDetails).filter_by(id=trip_id).one()
        return trip

    def put(self, trip_id):
        trip = db_session.query(TripsDetails).filter_by(id=trip_id).one()
        return trip

    def delete(self, trip_id):
        trip = db_session.query(TripsDetails).filter_by(id=trip_id).one()
        if not trip:
            session.delete(trip)

class DestinationAPI(Resource):
    def get(self, destination_id) :
        destination = db_session.query(TripsDetails).filter_by(id=destination_id).one()
        return destination

    def put(self, destination_id):
        destination = db_session.query(TripsDetails).filter_by(id=destination_id).one()
        return destination

    def delete(self, destination_id):
        destination = db_session.query(TripsDetails).filter_by(id=destination_id).one()
        if not destination:
            session.delete(destination)

api.add_resource(UserAPI, '/user_api/<int:user_id>')
api.add_resource(TripAPI, '/trip_api/<int:trip_id>')
api.add_resource(DestinationAPI, '/destination_api/<int:destination_id>')

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
