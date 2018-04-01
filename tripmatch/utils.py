from datetime import datetime
from functools import wraps

from flask import session as login_session, flash
from flask import g, redirect, url_for

from wtforms import Form, validators, StringField, PasswordField, BooleanField


def login_required(f: object) -> object:
    """
    Decorator for pages that requires user login
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if login_session.get('user_id', None) is None:
            return redirect(url_for('timeline.login'))
        g.user = login_session.get('user_id')
        return f(*args, **kwargs)

    return decorated_function


def get_current_datetime_string():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


def format_date_to_string(dt):
    return datetime.strptime(dt, '%Y-%m-%d')


class RegistrationForm(Form):
    username = StringField(u'Username', validators=[validators.Length(min=4, max=25)])
    email = StringField(u'Email', validators=[validators.Length(min=6, max=35), validators.email()])
    password = PasswordField(u'Password', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=30),
        validators.EqualTo('repeat_password', message='Passwords must match')
    ])
    repeat_password = PasswordField(u'Repeat_password')


class LoginForm(Form):
    username = StringField(u'Username', [validators.Length(min=4, max=25)])
    password = PasswordField(u'Password', [validators.DataRequired()])
    remember_me = BooleanField(u'Remember_me')


def flash_error(form):
    for field, errors in form.errors.item():
        for error in errors:
            flash(u'Error in the %s field - %s' % (getattr(form, field).label.text, error))
