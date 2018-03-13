import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .tripmatch_model import Base


def init_app(app):
    engine = create_engine(app.config['DATABASE_URI'], connect_args={'check_same_thread': False})

    # create tables
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    # Session = scoped_session(sessionmaker(bind=engine))  # This is a global session
    return session_factory


