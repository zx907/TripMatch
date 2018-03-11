import os

APPLICATION_NAME = 'Trip Match'
SECRET_KEY = 'secret key'
DEBUG = False
EXPLAIN_TEMPLATE_LOADING = False
SQLALCHEMY_ECHO = False
DATABASE_URI = 'sqlite://:memory:'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tripmatch', 'static', 'user_uploaded_photos')
ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}
