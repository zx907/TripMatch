from flask import Flask, g
from flask import session as login_session


def create_app(config_filename):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)

    from .db import init_app

    from .app import timeline
    from .manage import manage
    from .api import api

    app.register_blueprint(timeline)
    app.register_blueprint(manage)
    app.register_blueprint(api)

    session_factory = init_app(app)

    @app.before_request
    def before_request():
        g.user = login_session.get('user_id', None)
        db_session = session_factory()
        g.db_session = db_session

    @app.teardown_appcontext
    def close_db(error):
        if hasattr(g, 'db_session'):
            g.db_session.close()

    return app


