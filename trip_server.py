from flask import Flask, g
from flask import render_template, url_for, redirect, flash
from flask import session as login_session
from flask import make_response, Response, request
from flask import json, jsonify
from flask import abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tripmatch_model import Base, User, TripDetails
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash, gen_salt
import requests
import random
import string
import time

PER_PAGE = 30
DEBUG = True

# database engine and session
engine = create_engine("sqlite:////testdb.db")
# create tables
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
db_session = Session()


# configuration
APPLICATION_NAME = "Trip Match"
app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('TRIPMATCH_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.user = None
    if 'username' in login_session:
        g.user = db_session.query(User).filter(User.username==login_session['username']).first()


@app.route('/')
def timeline(): 
    trips = db_session.query(TripDetails).all()    
    return render_template('timeline.html', trips=trips)



@app.route('/public')
def public_timeline():
    trips = db_session.query(TripDetails).all()    
    return render_template('timeline.html', trips=trips)


@app.route('/add_trip', methods=['POST'])
def add_trip():
    print("hello")
    if 'username' not in login_session:
        abort(401)

    new_trip = TripDetails( username=login_session['username'],
                            country=request.form['country'],
                            state=request.form['state'],
                            city=request.form['city'],
                            duration=request.form['duration'],                                         
                            date_start=request.form['date_start'],
                            companions=request.form['companions'],
                            city_takeoff=request.form['city_takeoff'])
    db_session.add(new_trip)
    db_session.commit()
    flash('Your trip is posted')

    return redirect(url_for('timeline'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        user = db_session.query(User).filter(User.username==request.form['username']).first()
        if user is None:
            error = 'invalid username'
        elif not check_password_hash(user.password, request.form['password']):
            error = 'invalid password'
        else:
            flash ('you were logged in')
            login_session['username'] = user.username
            return redirect(url_for('timeline'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        print(g.user)
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'Please enter a username'
        elif not request.form['email']:
            error = 'Please enter an email address'
        elif not request.form['password']:
            error = 'Please enter a password'
        elif request.form['password']!=request.form['password2']:
            error = 'Passwords are not matched'
        elif UsernameExists(request.form['username']) is not None:
            error = 'The username is already taken'
        elif EmailExists(request.form['email']):
            error = 'The email address is already taken'
        else:
            new_user = User(
                username=request.form['username'], email=request.form['email'], password=
                generate_password_hash(request.form['password']))
            db_session.add(new_user)
            db_session.commit()
            flash('Register successfully')
            return redirect(url_for('login'))

    return render_template('register.html')


def EmailExists(email):
    return db_session.query(User.email).filter(User.email == email).scalar()


def UsernameExists(username):
    return db_session.query(User.email).filter(User.username == username).scalar()


if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    app.run(host='127.0.0.1', port=5000, debug=True)
