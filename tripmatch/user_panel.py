from flask import Blueprint
from flask import render_template, redirect, url_for, abort
from flask import session as login_session

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

@admin.route(/)
def account():
    user = 
