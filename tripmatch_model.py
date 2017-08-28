from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return "<User(username='%s', email='%s', password='%s')>" % (self.name, self.fullname, self.password)


class TripDetails(Base):
    """
        username
        country
        state
        city
        duration
        date_start
        companions
        city_takeoff
    """
    __tablename__ = 'trip_details'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    country = Column(String, nullable=False)
    state = Column(String, nullable=True)
    city = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    date_start = Column(String, nullable=False)
    companions = Column(Integer, nullable=False)
    city_takeoff = Column(String, nullable=True)

    def __repr__(self):
        "<TripDetails(username='%s', country='%s', state='%s', city='%s', duration='%s', date_start='%s', companion='%s', city_takeoff='%s')>" \
        % (self.username, self.country, self.state, self.city, self.duration, self.date_start, self.companions, self.city_takeoff)


# class Cities(Base):
#     __table__ = 'cities'
#     id = Column(Integer, primary_key=True)
#     city_name = Column(String, nullable=False)

# class Countries(Base):
#     __table__ = 'countries'
#     id = Column(Integer, primary_key=True)
#     country_name = Column(String, nullable=False)