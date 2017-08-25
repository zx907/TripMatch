from flask import Flask, g
from flask import render_template, url_for, redirect, flash
from flask import session as login_session
from flask import make_response, Response, request
from flask import json, jsonify
from flask import abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tripmatch_model import Base, User
from datetime import datetime
import requests
import random
import string
import time

PER_PAGE = 30
DEBUG = True

# database engine and session
engine = create_engine("sqlite://testdb.db")
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)()

# configuration
APPLICATION_NAME = "Trip Match"
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('TRIPMATCH_SETTINGS', silent=True)

@app.route('/')
def timeline():
    return render_template('tripmatch.html')



@app.route('/public')
def public_timeline():
    return render_template('timeline.html')


@app.route('/add_trip', methods=['POST'])
def add_trip():
    if 'user_id' not in login_session:
        abort(401)
    if request.form['text']:
        flash('Your trip info was saved')
    return redirect(url_for('timeline'))

@app.route('/login', methods=['GET','POST'])
def login():
    if g.user:
        redirect(url_for('timeline')) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.methond == 'POST':
        if not request.form['username']:
            error = 'Please enter a username'
        elif not request.form['email']:
            error = 'Please enter an email address'
        elif not request.form['password']:
            error = 'Please enter a password'
        elif getUserId(request.form['username']) is not None:
            error = 'The username is already taken'
        elif checkEmailExist(request.form['email']):
            error = 'The email address is already taken'
        else:
            new_user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'])
            db_session.add(new_user)
            db_session.commit()
            flash('Register successfully')
            return redirect(url_for('login'))
    
    return render_template('register.html', error=error)

def checkEmailExist(email):
    exists = session.query(User.email).filter(User.email = email).scalar()



if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    app.run(host='127.0.0.1', port=5000, debug=True)

