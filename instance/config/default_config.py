import os

APPLICATION_NAME = 'Trip Match'
SECRET_KEY = 'secret key'
ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}
PER_PAGE = 12
# -----------------------------------------------
DATABASE_URI = 'sqlite:///{0}/testdb.db'.format(os.getcwd())
DEBUG = False
EXPLAIN_TEMPLATE_LOADING = False
SQLALCHEMY_ECHO = False

