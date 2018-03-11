import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .tripmatch_model import Base

# database engine and session
engine = create_engine("sqlite:///" + os.getcwd() +
                       "/testdb.db", connect_args={'check_same_thread': False})
# create tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)