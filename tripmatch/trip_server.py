from flask import Flask, g, app
from flask import render_template, url_for, redirect, flash
from flask import session as login_session
from flask import make_response, Response, request
from flask import json, jsonify
from flask import abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import ClauseElement
from tripmatch_model import Base, Users, TripDetails, Messages, Waitinglist, Destinations, TripToDestination
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
engine = create_engine("sqlite:////testdb.db")


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
    trips = db_session.query(Messages, TripDetails,
                             Users).order_by(Messages.id).all()
    return render_template('timeline.html', trips=trips)


@app.route('/public')
def public_timeline():
    db_session = get_db_session()
    trips = db_session.query(TripDetails).all()
    return render_template('timeline.html', trips=trips)


@app.route('/display_trip')
def display_trip(trip_id):
    db_session = get_db_session()
    trip = db_session.query(TripDetails).filter_by(id=trip_id).one()
    return render_template('trip_detail.html', trip=trip)


@app.route('/new_trip', methods=['GET', 'POST'])
def new_trip():
    if 'user_id' not in login_session:
        abort(401)

    try:
        db_session = get_db_session()
        destination_id = get_or_create(db_session, Destinations, {'destination':request.form['destination']})[0]
        # destination_query = db_session.query(Destinations).filter_by(destination=request.form['destination']).first()
        # if destination_query == None:
        #     new_destination = Destinations(destination=request.form['destination'])
        # else:
        #     destination_id = destination_query.id

        new_trip = TripDetails(user_id=login_session['user_id'],
                               destination_id=destination_id,
                               duration=request.form['duration'],
                               date_start=request.form['date_start'],
                               companions=request.form['companions'],
                               city_takeoff=request.form['city_takeoff'],
                               expected_group_size=request.form['expected_group_size'],
                               notes=request.form['notes']
                               )

        db_session.add(new_trip)
        db_session.commit()
        flash('Your trip is posted')
    except:
        db_session.rollback()
        flash('Your trip is posted unsuccessfully')

    return redirect(url_for('timeline'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.get('user', None) != None:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        db_session = get_db_session()
        user = db_session.query(Users).filter(
            Users.username == request.form['username']).first()
        if user is None:
            error = 'invalid username'
        elif not check_password_hash(user.password, request.form['password']):
            error = 'invalid password'
        else:
            flash('you were logged in')
            login_session['username'] = user.username
            return redirect(url_for('timeline'))
    return render_template('login.html')


app.route('/logout')


def logout():
    login_session.pop(login_session['username'], None)
    flash('You were logged out')
    return redirect(url_for('public_timeline'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.get('user', None) != None:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        db_session = get_db_session()
        if not request.form['username']:
            error = 'Please enter a username'
        elif not request.form['email']:
            error = 'Please enter an email address'
        elif not request.form['password']:
            error = 'Please enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'Passwords are not matched'
        elif UsernameExists(request.form['username']) is not None:
            error = 'The username is already taken'
        elif EmailExists(request.form['email']):
            error = 'The email address is already taken'
        else:
            new_user = Users(
                username=request.form['username'], email=request.form['email'], password=generate_password_hash(request.form['password']))
            db_session.add(new_user)
            db_session.commit()
            flash('Register successfully')
            return redirect(url_for('login'))

    return render_template('register.html')


def EmailExists(email):
    db_session = get_db_session()
    return db_session.query(Users.email).filter(Users.email == email).scalar()


def UsernameExists(username):
    db_session = get_db_session()
    return db_session.query(Users.email).filter(Users.username == username).scalar()

def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True

if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
