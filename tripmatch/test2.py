from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import ClauseElement
from tripmatch_model import Base, Users, TripDetails, Messages, Waitinglist, Destinations, TripToDestination

engine = create_engine("sqlite:////testdb.db", connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True

session = Session()

x = get_or_create(session, Destinations, destination='Hainan')
print(x)
print(x[0])
print(x[0].id)
print(x[0].destination)
print(x[1])
