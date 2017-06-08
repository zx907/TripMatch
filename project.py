import random
import string
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from model.test_result_model import UUT_TEST_INFO, LTE_RESULT
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from flask import make_response
from flask import json, jsonify
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import pymssql
import logging

app = Flask(__name__)

# Create database session
# engine = create_engine('sqlite:///restaurantmenuwithusers.db')
engine = create_engine("mssql+pymssql://pash_user:123456789@10.105.56.131/TESTSTAND")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = "Restaurant Menu App"

# logging.basicConfig(level=logging.DEBUG)

# Homepage
@app.route('/')
@app.route('/catalog')
def homepage():
    restaurants = session.query(Restaurant).all()
    return render_template('home_2.html', restaurants=restaurants)


# Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Facebook login page


@app.route('/fblogin')
def showFBLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login_fb.html', STATE=state)


# Display each restaurant menuitems
@app.route('/catalog/<restaurant>')
def displayRestaurant(restaurant):
    restaurants = session.query(Restaurant).all()
    current_restaurant_id = session.query(
        Restaurant).filter_by(name=restaurant).one().id
    menuitems = session.query(MenuItem).filter_by(
        restaurant_id=current_restaurant_id).all()
    return render_template('display_menuitems_2.html',
                           menuitems=menuitems,
                           restaurant=restaurant,
                           restaurants=restaurants)


# Add a new restaurant
@app.route('/catalog/new', methods=['POST', 'GET'])
def addRestaurant():
    # if 'username' not in login_session:
    #     return redirect(url_for('showLogin'))
    if request.method == 'POST':
        if session.query(Restaurant).filter_by(name=request.form['new_restaurant']).count() > 0:
            flash('This restaurant already exists, please choose another name')
            return render_template('new_restaurant_2.html')
        else:
            # restaurant = Restaurant(
            # name=request.form['new_restaurant'],
            # user_id=login_session['user_id'])
            restaurant = Restaurant(
                name=request.form['new_restaurant'])
            session.add(restaurant)
            session.commit()
            return redirect(url_for('homepage'))
    else:
        return render_template('new_restaurant_2.html')


# Edit restaurant, rename or delete
@app.route('/catalog/<restaurant>/edit', methods=['POST', 'GET'])
def editRestaurant(restaurant):
    # if 'username' not in login_session:
    #     redirect(url_for('showLogin'))
    if request.method == 'POST':
        session.query(Restaurant).filter_by(name=restaurant).update(
            {'name': request.form['restaurant_rename']})
        session.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template('edit_restaurant.html', restaurant=restaurant)


# Display menuitem description
@app.route('/catalog/<restaurant>/<menuitem_id>')
def displayMenuItem(restaurant, menuitem_id):
    # restaurant_id = session.query(Restaurant).filter_by(name=restaurant).one().id
    one_menuitem = session.query(MenuItem).filter_by(id=menuitem_id).one()
    return render_template('menuitem_description_2.html',
                           one_menuitem=one_menuitem,
                           restaurant=restaurant)


# Add a new menuitem to a restaurant
@app.route('/catalog/<restaurant>/new', methods=['POST', 'GET'])
def addMenuItem(restaurant):
    # if 'username' not in login_session:
    #     return redirect(url_for('showLogin'))
    if request.method == 'POST':
        if session.query(MenuItem).filter_by(name=request.form['new_menuitem']).count() > 0:
            flash('This menuitem already exists, please choose another menuitem name')
            return render_template('new_menuitem_2.html')
        else:
            current_restaurant_id = session.query(
                Restaurant).filter_by(name=restaurant).one().id
            menuitem = MenuItem(
                name=request.form['new_menuitem'], restaurant_id=str(current_restaurant_id))
            session.add(menuitem)
            session.commit()
            return redirect(url_for('displayRestaurant', restaurant=restaurant))
    else:
        return render_template('new_menuitem_2.html', restaurant=restaurant)


# Edit menuitem description
@app.route('/catalog/<restaurant>/<menuitem_id>/edit', methods=['POST', 'GET'])
def editMenuItem(restaurant, menuitem_id):
    # if 'username' not in login_session:
    #     return redirect(url_for('showLogin'))
    if request.method == 'POST':
        if request.form.get['btn_save', None] == 'Save':
            session.query(MenuItem).filter_by(id=menuitem_id).update(
                {'description': request.form['description_text']})
            session.commit()
        if request.form.get['btn_save', None] == 'Delete':
            session.query(MenuItem).filter_by(id=menuitem_id).delete()
            session.commit()
        else:
            return redirect(url_for('displayRestaurant', restaurant=restaurant))
    else:
        one_menuitem = session.query(MenuItem).filter_by(
            id=menuitem_id).one()  # get menuitem obj from menuitem id
        return render_template('edit_menuitem.html', restaurant=restaurant, menuitem=one_menuitem)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    print('enter gconnect')
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    # print('code: ', code)
    # print('code type: ', type(code))

    # Exchange code for token
    try:
        print('try oauth_flow')
        oauth_flow = flow_from_clientsecrets(
            'client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        h1 = httplib2.Http(proxy_info=httplib2.ProxyInfo(
            proxy_type='PROXY_TYPE_SOCKS5', proxy_host='127.0.0.1', proxy_port=1080))
        credentials = oauth_flow.step2_exchange(code.decode(), http=h1)
        print('credentials: ', credentials)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token

    # Verify token
    print('Start Verification')
    # Add shadowsocks proxy for httplib2
    h = httplib2.Http(proxy_info=httplib2.ProxyInfo(
            proxy_type='PROXY_TYPE_SOCKS5', proxy_host='127.0.0.1', proxy_port=1080))
    url = ('https://www.googleapis.com/oauth2/v3/userinfo?access_token=%s' %
           access_token)
    # x = h.request(url, 'GET')[1]
    resp_json = h.request(url, 'GET')
    print(resp_json) 
    # print('============')
    result = json.loads(str(x, 'utf8'))
    # print(type(result))
    # print(result)

    # for k,v in result.items():
    #     print(k, v)
    # print('=============')

    gplus_id = credentials.id_token['sub']
    if result['sub'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print('OK')

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # print('result error check --- OK')
    # print('<'*10)

    # for k,v in login_session.items():
    #     print(k,v)
    # print('<'*10)

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print('stored credential is not None, already logged in')
        return response

    # print('stored_credentials: ', stored_credentials)
    # print('stored_gplus_id: ', stored_gplus_id)
    # print('stored credentials check --- OK')

    # print('LoginSession: ', login_session)
    # print('LoginSession type: ', type(login_session))
    # print('++++++++++++++++++++++')

    login_session['provider'] = 'google'
    login_session['token'] = access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token}
    answer = requests.get(userinfo_url, params=params)
    # print('answer type: ' ,type(answer))
    # print(answer.status_code)
    # print(answer.json())
    # print(type(answer.json()))
    data = answer.json()
    # print('data: ', data)
    # print('++++++++++++++++++++++')

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # print('get info --- OK')

    # response = make_response('good 1', 200)
    # response.headers['Content-Type'] = 'application/json'
    # return response
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    if credentials is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['token']
        del login_session['gplus_id']
        del login_session['provider']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps("Successfully disconnected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps("Failed to revode token"), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    print("enter fbconncet")
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps("invalid state parameter."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    print('1')
    print("access token received %s " % access_token)

    # Get Long-lived token
    app_id = json.loads(open('client_secrets_fb.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(open('client_secrets_fb.json', 'r').read())[
        'web']['app_secret']
    # url = """/oauth/access_token?
    #          grant_type=fb_exchange_token&amp;
    #          client_id=%s&amp;
    #          client_secret=%s&amp;
    #          fb_exchange_token=%s""" % (app_id, app_secret, access_token)

    url = 'https://graph.facebook.com/oauth/\
        access_token?grant_type=fb_exchange_token&\
        client_id=%s&\
        client_secret=%s&\
        fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    print('2')

    userinfo_url = "https://graph.facebook.com/v2.5/me"
    token = result.split("&")[0]  # Long-lived token

    # Get user info
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    print('3')
    data = json.loads(result)
    login_session['username'] = data["name"]
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    login_session['provider'] = 'facebook'

    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get profile picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data['data']['url']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['picture']
    del login_session['email']
    del login_session['user_id']
    del login_session['facebook_id']
    return "You have been logged out"


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        # del login_session['username']
        # del login_session['email']
        # del login_session['picture']
        # del login_session['user_id']
        # del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('homepage'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('homepage'))


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(user_email):
    try:
        user = session.query(User).filter_by(email=user_email).one()
        return user.id
    except:
        return None

@app.route('/qyer', methods=['GET', 'POST'])
def qyer():
    return render_template('fuck.html')


@app.route('/getJSONResult', methods=['GET', 'POST'])
def getJSONResult():

    if request.method == 'POST':
        uut = request.form['uut']
        notes = request.form['notes']
        temperature = request.form['temperature']

        logging.info("Enter getJSONResult")
        print("Enter getJSONResult")

        filter_by_query = {k: v for k, v in {
            'uut': uut, 'notes': notes, 'temperature': temperature}.items() if v != ""}

        s = session.query(UUT_TEST_INFO).filter_by(**filter_by_query).first()
        # s = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7}
        return jsonify(s.serialize)




if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
