from flask import flash
from wtforms import Form, StringField, PasswordField, validators, BooleanField


class RegistrationForm(Form):
    username = StringField(u'Username', validators=[validators.Length(min=4, max=25)])
    email = StringField(u'Email', validators=[validators.Length(min=6, max=35), validators.email()])
    password = PasswordField(u'Password', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=30),
        validators.EqualTo('repeat_password', message='Passwords must match')
    ])
    repeat_password = PasswordField(u'Repeat password')


class LoginForm(Form):
    username = StringField(u'Username', [validators.Length(min=4, max=25)])
    password = PasswordField(u'Password', [validators.DataRequired()])
    remember_me = BooleanField(u'Remember_me')


def flash_error(form):
    for field, errors in form.errors.item():
        for error in errors:
            flash(u'Error in the %s field - %s' % (getattr(form, field).label.text, error))