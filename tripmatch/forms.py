from flask import flash
from wtforms import Form, StringField, PasswordField, validators, BooleanField, SubmitField, IntegerField, DateField, \
    TextAreaField, FileField


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
    remember_me = BooleanField(u'Remember Me')
    submit = SubmitField(u'Sign In')

class TripForm(Form):
    destination = StringField(u'Destination')
    duration = IntegerField(u'Duration')
    date_start = DateField(u'Start Date')
    date_end = DateField(u'End Date')
    companions = IntegerField(u'Companions')
    city_takeoff = StringField(u'Leaving From')
    expected_group_size = IntegerField(u'Expect Group Size')
    notes = TextAreaField(u'Notes')
    contact = StringField(u'Contact')
    img_name = FileField(u'Cover Image')
    submit = SubmitField(u'Post')


def flash_error(form):
    for field, errors in form.errors.item():
        for error in errors:
            flash(u'Error in the %s field - %s' % (getattr(form, field).label.text, error))