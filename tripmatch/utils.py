from datetime import datetime
from functools import wraps

from flask import session as login_session
from flask import g, redirect, url_for, request


def login_required(f: object) -> object:
    """
    Decorator for pages that requires user login
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if login_session['user_id'] is None:
            return redirect(url_for('login', next=request.url))
        g.user = login_session.get('user_id')
        return f(*args, **kwargs)

    return decorated_function


def get_current_datetime_string():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def format_date_to_string(dt):
    return datetime.strptime(dt, '%Y-%m-%d')
