import os

APPLICATION_NAME = 'Trip Match'
SECRET_KEY = 'secret key'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tripmatch', 'static', 'user_uploaded_photos')
ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}
PER_PAGE = 12
# --------------------------------------------------
DATABASE_URI = 'sqlite:///{0}/testdb.db'.format(os.getcwd())
DEBUG = True
EXPLAIN_TEMPLATE_LOADING = True
SQLALCHEMY_ECHO = True
