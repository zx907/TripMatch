from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    trip_details = relationship('TripDetails', back_populates='users')
    waitinglist = relationship('Waitinglist', back_populates='users')

    def to_dict(self):
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {'id': self.id, 'username': self.username, 'email': self.email}  # don't wanna include password

    def __repr__(self):
        return "<User(username='%s', email='%s', password='%s')>" % (self.username, self.email, self.password)

    user_dest_association_tbl = Table('usr_dest_as_tbl', Base.metadata,
                                      Column('user_id', Integer, ForeignKey('users.id')),
                                      Column('destination_id', Integer, ForeignKey('destinations.id'))
                                      )


class TripDetails(Base):
    """username, country, state, destination, duration, date_start, companions, city_takeoff"""
    __tablename__ = 'trip_details'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    destination_id = Column(Integer, ForeignKey('destinations.id'))
    duration = Column(String, nullable=True)
    date_start = Column(String, nullable=False)
    companions = Column(Integer, nullable=False)
    city_takeoff = Column(String, nullable=True)
    expected_group_size = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    date_create = Column(String, nullable=False)
    contact = Column(String, nullable=True)
    img_name = Column(String, nullable=True)

    users = relationship('Users', back_populates='trip_details')
    destinations = relationship('Destinations', back_populates='trip_details')
    waitinglist = relationship('Waitinglist', back_populates='trip_details')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_dict_ex(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['username'] = self.users.username
        d['destination'] = self.destinations.destination
        return d

    def __repr__(self):
        "<TripDetails(username='%s', destination='%s', duration='%s', date_start='%s', companion='%s', city_takeoff='%s', expected_group_size='%s', notes='%s')>" \
        % (self.username, self.destination, self.duration, self.date_start, self.companions, self.city_takeoff,
           self.expected_group_size, self.notes)


class Destinations(Base):
    """destination: String"""
    __tablename__ = 'destinations'
    id = Column(Integer, primary_key=True)
    destination = Column(String, nullable=False)

    trip_details = relationship('TripDetails', back_populates='destinations')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Waitinglist(Base):
    __tablename__ = 'waitinglist'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    trip_id = Column(Integer, ForeignKey('trip_details.id'))
    text = Column(String, nullable=False)
    post_date = Column(String, nullable=False)

    users = relationship('Users', back_populates="waitinglist")
    trip_details = relationship('TripDetails', back_populates="waitinglist")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class InMails(Base):
    __tablename__ = 'inmails'
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, nullable=False)
    to_id = Column(Integer, nullable=False)
    inmail_title = Column(String, nullable=False)
    inmail_text = Column(String, nullable=False)
    send_date = Column(String, nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
