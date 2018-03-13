import os

APPLICATION_NAME = 'Trip Match'
SECRET_KEY = 'secret key'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tripmatch', 'static', 'user_uploaded_photos')
ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}
PER_PAGE = 12
# ------------------------------------------------------
DATABASE_URI = 'postgresql://postgres:654321@localhost/tripmatch_database'
DEBUG = False
EXPLAIN_TEMPLATE_LOADING = False
SQLALCHEMY_ECHO = False
