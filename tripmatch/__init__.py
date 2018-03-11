import os

from flask import Flask, g
from flask import session as login_session

from .app import timeline
from .manage import manage
from .api import api
from .config import config

app = Flask(__name__)

app.config.from_object(config['development'])
# app.config.from_envvar('TRIPMATCH_SETTINGS')



# PER_PAGE = 12
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tripmatch', 'static', 'user_uploaded_photos')
ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}

# configuration
# APPLICATION_NAME = 'Trip Match'
# app.secret_key = ''.join(random.choice(
#     string.ascii_uppercase + string.digits) for x in range(32))
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True


app.register_blueprint(timeline)
app.register_blueprint(manage)
app.register_blueprint(api)

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('applogger')


@app.before_request
def before_request():
    g.user = login_session.get('user_id', None)