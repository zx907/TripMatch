APPLICATION_NAME = 'Trip Match'
SECRET_KEY = 'secret key'
ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}
PER_PAGE = 12
# --------------------------------------------------
# DATABASE_URI = 'sqlite:///{0}/testdb.db'.format(os.getcwd())
# DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, '..', '..', 'testdb.db')
DATABASE_URI = 'postgresql://tripmatch_user:123456@localhost/tripmatch_db'
DEBUG = True
# EXPLAIN_TEMPLATE_LOADING = True
SQLALCHEMY_ECHO = True
# --------------------------------------
CELERY_BROKER_URL='redis://localhost:6379',
CELERY_RESULT_BACKEND='redis://localhost:6379'