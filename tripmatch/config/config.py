import os


class DefaultConfig:
    APPLICATION_NAME = 'Trip Match'
    SECRET_KEY = 'secret key'
    DEBUG = False
    EXPLAIN_TEMPLATE_LOADING = False
    SQLALCHEMY_ECHO = False
    DATABASE_URI = 'sqlite://:memory:'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tripmatch', 'static', 'user_uploaded_photos')
    ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}
    PER_PAGE = 12


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    EXPLAIN_TEMPLATE_LOADING = True
    SQLALCHEMY_ECHO = True
    DATABASE_URI = "sqlite:///{0}/testdb.db".format(os.getcwd())


class ProductionConfig(DefaultConfig):
    DEBUG = False
    EXPLAIN_TEMPLATE_LOADING = False
    SQLALCHEMY_ECHO = False


config = {
    'default': DefaultConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
