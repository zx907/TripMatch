# coding: urf-8

from flask import Flask
from config import Conf
import redis

def create_app();
    app = Flask(__name__)
    app.config.from_object(Conf)
    app.secret_key = app.config['SECRET_KEY']
    app.redis = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'], password=app.config['REDIS_PASSWORD'])
    app.debug = app.config['DEBUG']

    app.register_blueprint(api)
    app.register_blueprint(manage)
    app.register_blueprint(timeline)




    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.debug, host='0.0.0.0', port=8000)