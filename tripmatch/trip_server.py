from flask import Flask, g, app
from flask import render_template, url_for, redirect, flash
from flask import session as login_session
from flask import make_response, Response, request
from flask import json, jsonify
from flask import abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import ClauseElement
from tripmatch_model import Base, Users, TripDetails, Waitinglist, Destinations
from werkzeug.security import check_password_hash, generate_password_hash, gen_salt
from datetime import datetime
import requests
import random
import string

PER_PAGE = 30
DEBUG = True

# configuration
APPLICATION_NAME = 'Trip Match'
# TRIPMATCH_SETTINGS = 'settings.txt'
app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.from_envvar('TRIPMATCH_SETTINGS', silent=True)

# database engine and session
engine = create_engine("sqlite:////testdb.db", connect_args={'check_same_thread': False})


# create tables
def init_db():
    Base.metadata.create_all(engine)


def get_db_session():
    return sessionmaker(bind=engine)()


# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'db_session'):
#         g.db_session.close()


# @app.before_request
# def before_request():
#     g.user = None
#     if 'username' in login_session:
#         db_session = get_db_session()
#         g.user = db_session.query(Users).filter(Users.username==login_session['username']).first()


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


@app.route('/trip_detail/<int:trip_id>')
def display_trip(trip_id):
    db_session = get_db_session()
    trip = db_session.query(TripDetails).filter_by(id=trip_id).one()
    waitinglist = db_session.query(Waitinglist).filter_by(trip_id=trip_id).all()
    return render_template('trip_details.html', trip=trip, waitinglist=waitinglist)


@app.route('/new_trip', methods=['GET', 'POST'])
def new_trip():
    if 'user_id' not in login_session:
        abort(401)

    if request.method == 'POST':

        db_session = get_db_session()
        try:
            destination = get_or_create(
                db_session,
                Destinations,
                destination=request.form['destination']
            )[0]
            # print(destination.id)
            # print(destination.destination)

            # destination_query = db_session.query(Destinations).filter_by(destination=request.form['destination']).first()
            # if destination_query == None:
            #     new_destination = Destinations(destination=request.form['destination'])
            # else:
            #     destination_id = destination_query.id

            date_create = datetime.now().isoformat(' ')

            new_trip = TripDetails(user_id=login_session['user_id'],
                                destination_id=destination.id,
                                duration=request.form['duration'],
                                date_start=request.form['date_start'],
                                companions=request.form['companions'],
                                city_takeoff=request.form['city_takeoff'],
                                expected_group_size=request.form['expected_group_size'],
                                notes=request.form['notes'],
                                date_create=date_create
                                )


            db_session.add(new_trip)
            db_session.commit()
            flash('Your trip is posted')
        except Exception as e:
            db_session.rollback()
            print(e)
            flash('Your trip is posted unsuccessfully')

    return render_template('new_trip.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if login_session.get('user_id', None) != None:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        db_session = get_db_session()
        user = db_session.query(Users).filter(
            Users.username==request.form['username']).first()
        if user == None:
            error = 'invalid username'
            flash('invalid username')
        elif not check_password_hash(user.password, request.form['password']):
            error = 'invalid password'
            flash('invalid password')
        else:
            flash('you were logged in')
            login_session['user_id'] = user.id
            return redirect(url_for('timeline'))
    return render_template('login.html')


app.route('/logout')
def logout():
    login_session.pop(login_session['user_id'], None)
    flash('You were logged out')
    return redirect(url_for('public_timeline'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if login_session.get('user_id', None) != None:
        return redirect(url_for('timeline'))
    error = None
    if request.method=='POST':
        if not request.form['username']:
            error = 'Please enter a username'
        elif UsernameExists(request.form['username']):
            error = 'The username is already taken'
        elif not request.form['email']:
            error = 'Please enter an email address'
        elif EmailExists(request.form['email']):
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
            except :
                db_session.rollback()
                flash('Registion failed') 
                return redirect(url_for('timeline'))

    return render_template('register.html')


@app.route('/join_waitinglist', methods=['POST'])
def join_waitinglist():
    if login_session.get('user_id', None) == None:
        return redirect(url_for('login'))
    if request.method=='POST':
        text = request.form['message']
        user_id = login_session['user_id']
        trip_id = request.form['trip_id']
        post_date = date_create = datetime.now().isoformat(' ')

        db_session = get_db_session()
        try:
            new_wtl_entry = Waitinglist(
                user_id=user_id, trip_id=trip_id, text=text, post_Date=post_date)
            db_session.add(new_wtl_entry)
            db_session.commit() 
        except:
            db_session.rollback()
            

def EmailExists(email):
    db_session = get_db_session()
    return db_session.query(Users).filter(Users.email == email).first()


def UsernameExists(username):
    db_session = get_db_session()
    return db_session.query(Users).filter(Users.username == username).first()


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True

if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
