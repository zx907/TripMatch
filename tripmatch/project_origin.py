from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Create database session
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu App"


# Homepage
@app.route('/')
@app.route('/catalog')
def homepage():
    restaurants = session.query(Restaurant).all()
    return render_template('home_2.html', restaurants=restaurants)


# Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Facebook login page
@app.route('/fblogin')
def showFBLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login_fb.html', STATE=state)


# Display each restaurant menuitems
@app.route('/catalog/<restaurant>')
def displayRestaurant(restaurant):
    restaurants = session.query(Restaurant).all()
    current_restaurant_id = session.query(Restaurant).filter_by(name=restaurant).one().id
    menuitems = session.query(MenuItem).filter_by(restaurant_id=current_restaurant_id).all()
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
            restaurant = Restaurant(name=request.form['new_restaurant'], user_id=login_session['user_id'])
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
        session.query(restaurant).filter_by(name=restaurant).update({'name': request.form['restaurant_rename']})
        session.commit()
        return redirect(url_for(homepage))
    else:
        return render_template(url_for('edit_restaurant.html', restaurant=restaurant))


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
            current_restaurant_id = session.query(Restaurant).filter_by(name=restaurant).one().id
            menuitem = MenuItem(name=request.form['new_menuitem'], restaurant_id=str(current_restaurant_id))
            session.add(menuitem)
            session.commit()
            return redirect(url_for('displayRestaurant', restaurant=restaurant))
    else:
        return render_template('new_menuitem_2.html', restaurant=restaurant)


# Edit menuitem description
@app.route('/catalog/<restaurant>/<menuitem>/edit', methods=['POST', 'GET'])
def editMenuItem(restaurant, menuitem):
    if 'username' not in login_session:
         return redirect(url_for('showLogin'))
    if request.method == 'POST':
        if request.form.get['btn_save', None] == 'Save':
            session.query(MenuItem).filter_by(name=menuitem).update({'description': reqeust.form['description_text']})
            session.commit()
        if request.form.get['btn_save', None] == 'Delete':
            session.query(MenuItem).filter_by(name=menuitem).delete()
            session.commit()
        else:
            return redirect(url_for('displayRestaurant', restaurant=restaurant))
    else:
        return render_template('edit_menuitem.html', restaurant=restaurant, menuitem=menuitem)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    print('enter gconnect')
    # if request.args.get('state') != login_session['state']:
        # response = make_response(json.dumps('invalid state'), 401)
        # response.headers['Content-Type'] = 'application/json'
        # return response
    code = request.data
    print('code: ', code)
    print('code type: ', type(code))
    
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'

        credentials = oauth_flow.step2_exchange(code.decode())
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    response = make_response('good 1', 200)
    response.headers['Content-Type'] = 'application/json'
    return response
    # access_token = credentials.access_token
    # url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    # h = httplib2.Http()
    # xxx = h.request(url, 'GET')[1].decode()
    # print('xxx type: ', type(xxx))
    # result = json.loads(xxx)
    # if result.get('error') is not None:
        # response = make_response(json.dumps(result.get('error')), 500)
        # response.headers['Content-Type'] = 'application/json'
        # return response
    # gplus_id = credentials.id_token['sub']
    # if result['user_id'] != gplus_id:
        # response = make_response(json.dumps("Token's user ID doesn't match given user ID"), 401)
        # response.headers['Content-Type'] = 'application/json'
        # return response
    # if result['issued_to'] != CLIENT_ID:
        # response = make_response(json.dumps("Token's client ID doesn't match app's ID"), 401)
        # response.headers['Content-Type'] = 'application/json'
        # return response
    # stored_credentials = login_session.get('credentials')
    # stored_gplus_id = login_session.get('gplus_id')
    # if stored_credentials is not None and gplus_id == stored_gplus_id:
        # response = make_response(json.dumps('Current user is already connected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        
    # print('LoginSession: ', login_session)
    # print('LoginSession type: ', type(login_session))
    # login_session['provider'] = 'google'
    # login_session['credentials'] = credentials
    # login_session['gplus_id'] = gplus_id
    # userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    # params = {'access_token': credentials.access_token, 'alt': 'json'}
    # answer = requests.get(userinfo_url, params=params)
    # data = json.loads(answer.text)

    # login_session['username'] = data['name']
    # login_session['picture'] = data['picture']
    # login_session['email'] = data['email']
    
    # user_id = getUserID(login_session['email'])
    # if not user_id:
        # user_id = createUser(login_session)
    # login_session['user_id'] = user_id    

    # output = ''
    # output += '<h1>Welcome, '
    # output += login_session['username']
    # output += '!</h1>'
    # output += '<img src="'
    # output += login_session['picture']
    # output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # print("done!")
    # return output


@app.route('/gdisconnect')
def gdisconnect():
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token - credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
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
    print ("enter fbconncet")
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps("invalid state parameter."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    print ('1')
    print ("access token received %s " % access_token)


    # Get Long-lived token
    app_id = json.loads(open('client_secrets_fb.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('client_secrets_fb.json', 'r').read())['web']['app_secret']
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

    print ('2')


    userinfo_url = "https://graph.facebook.com/v2.5/me"
    token = result.split("&")[0]  # Long-lived token

    # Get user info
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    print ('3')
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
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
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


if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
