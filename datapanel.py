import random
import string
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from flask import make_response
import httplib2
import requests

app = Flask(__name__)

# Create database session
# engine = create_engine('sqlite:///restaurantmenuwithusers.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

APPLICATION_NAME = "Data Panel"

@app.route('/qyer')
def qyer():
    return render_template('framework.html')


if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
