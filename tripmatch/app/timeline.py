import os
from datetime import datetime, timedelta

from flask import current_app, g, Blueprint, render_template, url_for, redirect, flash, make_response, request
from flask import session as login_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import ClauseElement
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from ..db.tripmatch_model import Users, TripDetails, Waitinglist, Destinations
from ..utils import login_required


timeline = Blueprint('timeline', __name__)


@timeline.route('/')
def public_timeline():
    trips = g.db_session.query(TripDetails).all()
    return render_template('timeline.html', trips=trips)


@timeline.route('/trip_detail/<int:trip_id>', methods=['GET', 'POST'])
def display_trip(trip_id):
    if request.method == 'POST':  # Post to waiting list
        if login_session.get('user_id', None) is None:
            return redirect(url_for('.login'))
        text = request.form['leave-a-message-textarea']
        user_id = login_session['user_id']
        trip_id = request.form['trip_id']
        post_date = datetime.now().isoformat(' ')

        try:
            new_wtl_entry = Waitinglist(
                user_id=user_id, trip_id=trip_id, text=text, post_date=post_date)
            g.db_session.add(new_wtl_entry)
            g.db_session.commit()
        except SQLAlchemyError:
            g.db_session.rollback()

    trip = g.db_session.query(TripDetails).filter_by(id=trip_id).one()
    waitinglist = g.db_session.query(
        Waitinglist).filter_by(trip_id=trip_id).all()
    return render_template('trip_details.html', trip=trip, waitinglist=waitinglist)


@timeline.route('/new_trip', methods=['GET', 'POST'])
@login_required
def new_trip():
    # if 'user_id' not in login_session:
    #     redirect(url_for('.login'))

    # post new trip
    if request.method == 'POST':

        try:
            destination = get_or_create(
                g.db_session,
                Destinations,
                destination=request.form['destination']
            )[0]

            date_create = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

            new_trip = TripDetails(user_id=login_session['user_id'],
                                   destination_id=destination.id,
                                   duration=request.form['duration'],
                                   date_start=request.form['date_start'],
                                   companions=request.form['companions'],
                                   city_takeoff=request.form['city_takeoff'],
                                   expected_group_size=request.form['expected_group_size'],
                                   notes=request.form['notes'],
                                   date_create=date_create)

            file = request.files['new_trip_img_file']

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                new_trip.img_name = filename
            else:
                new_trip.img_name = None

            g.db_session.add(new_trip)
            g.db_session.commit()
            flash('Your trip is posted')
        except SQLAlchemyError as e:
            g.db_session.rollback()
            flash('Failed to post your trip')

    return render_template('new_trip.html')


# Pre-fill forms with existing information
@timeline.route('/edit_trip/<int:trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    if 'user_id' not in login_session:
        redirect(url_for('.login'))

    # update trip
    if request.method == 'POST':
        try:
            cur_trip = g.db_session.query(TripDetails).filter(TripDetails.id == trip_id).one()
            cur_trip.duration = request.form['duration']
            cur_trip.date_start = request.form['date_start']
            cur_trip.companions = request.form['companions']
            cur_trip.city_takeoff = request.form['city_takeoff']
            cur_trip.expected_group_size = request.form['expected_group_size']
            cur_trip.notes = request.form['notes']

            file = request.files['edited_trip_img_file']

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # check if filename already exists
                existing_files = [x for x in os.listdir(current_app.config['UPLOAD_FOLDER']) if
                                  os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], x))]
                suffix_index = 0
                while filename in existing_files:
                    filename = filename.split('.')[0] + '_' + str(suffix_index)
                    suffix_index += 1
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                cur_trip.img_name = filename

            g.db_session.commit()
            flash('Your trip is updated')

        except SQLAlchemyError as e:
            g.db_session.rollback()
            flash('Failed to update your trip')

    return render_template('edit_trip.html')


@timeline.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        dest_kw = request.form['jumbosearch']
        stmt = """
               SELECT
               trip_details.id, trip_details.destination_id, trip_details.date_create,
               trip_details.date_start, trip_details.duration,
               trip_details.img_name, destinations.destination
               FROM destinations LEFT JOIN trip_details
               ON destinations.id=trip_details.destination_id
               WHERE destinations.destination=\'{0}\';
               """.format(dest_kw)

        trips = g.db_session.execute(stmt)
        # conn = engine.connect()
        # trips = conn.execute(stmt)

        return make_response(render_template('search_result.html', trips=trips), 200,
                             {'Content-Type': 'text/html'})
    else:
        redirect(url_for('.public_timeline'))


@timeline.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log user in and save logged-in username in login_session dict
    """
    # app.logger.info('enter login')
    # redirect to home page if user has already been logged in
    if login_session.get('user_id', None):
        # app.logger.info(login_session['user_id'])
        return redirect(url_for('.public_timeline'))

    # Log user in
    if request.method == 'POST':
        user = g.db_session.query(Users).filter(
            Users.username == request.form['username']).first()
        if user is None:
            flash('invalid username')
        elif not check_password_hash(user.password, request.form['password']):
            flash('invalid password')
        # Add a cookie to response obj
        # elif request.form.get('remember_me', None) :
        #     print('set cookie')
        #     resp = make_response(redirect(url_for('public_timeline')))
        #     resp.set_cookie('tripmatch_user_id', str(user.id))
        #     login_session['user_id'] = user.id
        #     return resp
        else:
            flash('you were logged in')
            login_session['user_id'] = user.id
            # app.logger.info(login_session)
            return redirect(url_for('.public_timeline'))

    return render_template('login.html')


@timeline.route('/logout', methods=['GET', 'POST'])
def logout():
    # app.logger.info('enter logout')
    login_session.pop('user_id')
    # if request.cookie.get('user_id', None):
    #     resp = make_response(redirect(url_for('public_timeline')))
    #     resp.set_cookie('tripmatch_user_id', user.id, 0)
    #     flash('You were logged out')
    #     print('logout successful')
    #     return resp
    # else:
    flash('You were logged out')
    # app.logger.info(login_session)
    return redirect(url_for('.public_timeline'))


@timeline.route('/register', methods=['GET', 'POST'])
def register():
    # app.logger.info('enter register')
    if login_session.get('user_id', None) is not None:
        return redirect(url_for('.public_timeline'))

    # todo: considering replace following code with WTForm
    # todo: characters validation

    if request.method == 'POST':
        if not request.form['username']:
            flash('Please enter a username')
        elif username_exists(request.form['username']):
            flash('The username is already taken')
        elif not request.form['email']:
            flash('Please enter an email address')
        elif email_exists(request.form['email']):
            flash('The email address is already taken')
        elif not request.form['password']:
            flash('Please enter a password')
        elif request.form['password'] != request.form['password2']:
            flash('Passwords are not matched')
        else:
            try:
                new_user = Users(
                    username=request.form['username'], email=request.form['email'],
                    password=generate_password_hash(request.form['password']))
                g.db_session.add(new_user)
                g.db_session.commit()
                flash('Register successfully')
                login_session['user_id'] = request.form['username']  # automatically log user in after registration
                # app.logger.info(login_session)
                return redirect(url_for('.public_timeline'))
            except SQLAlchemyError:
                g.db_session.rollback()
                flash('Registration failure')
                return redirect(url_for('.public_timeline'))

    return render_template('register.html')


@timeline.route('/upload_trip_img', methods=['GET', 'POST'])
def upload_trip_img():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('.uploaded file', filename=filename))


@timeline.context_processor
def utility_processor():
    def calc_date_end(start_date, duration):
        return (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(int(duration))).strftime('%Y-%m-%d')

    return dict(calc_date_end=calc_date_end)


def email_exists(email):
    return g.db_session.query(Users).filter(Users.email == email).first()


def username_exists(username):
    return g.db_session.query(Users).filter(Users.username == username).first()


def item_exists(session, model, item):
    """
    query database with session and model to check if a specific item already exists in database
    :return: item or None
    """
    instance = session.query(model).filter_by(item).first()
    return instance


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items()
                      if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True


def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
