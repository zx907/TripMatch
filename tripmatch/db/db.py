import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .tripmatch_model import Base

# database engine and session
engine = create_engine("sqlite:///" + os.getcwd() +
                       "/testdb.db", connect_args={'check_same_thread': False})
# database engine and session
# engine = create_engine('postgresql://postgres:654321@localhost:5432/tripmatch_db')

# create tables
Base.metadata.create_all(engine)
sessionmaker(bind=engine)
# Session = scoped_session(sessionmaker(bind=engine))  # This is a global session

