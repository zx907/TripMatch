import os

_basedir = os.path.abspath(os.path.dirname(__file__))

APPLICATION_NAME = 'Trip Match'
SECRET_KEY = 'secret key'
UPLOAD_FOLDER = 'tripmatch/static/user_uploaded_photos'
ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}
PER_PAGE = 12
# --------------------------------------------------
# DATABASE_URI = 'sqlite:///{0}/testdb.db'.format(os.getcwd())
DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, '..', 'testdb.db')
DEBUG = True
EXPLAIN_TEMPLATE_LOADING = True
SQLALCHEMY_ECHO = True
