import os

APPLICATION_NAME = 'Trip Match'
SECRET_KEY = 'f09g93hg39hodf9HhYGOUY98685iGiYg23jrgfGYG246ZwdkvkwhevoHUH2f3vsd'
ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'png'}
PER_PAGE = 12
# ------------------------------------------------------
DATABASE_URI = 'postgresql://postgres:654321@localhost/tripmatch_database'
DEBUG = False
EXPLAIN_TEMPLATE_LOADING = False
SQLALCHEMY_ECHO = False
