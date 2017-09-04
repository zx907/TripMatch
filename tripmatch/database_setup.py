from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    restaurant = relationship("Restaurant", cascade="delete")
    menuitem = relationship('MenuItem', cascade="delete")

    @property
    def serialize(self):
        return {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    menuitem = relationship('MenuItem', cascade="delete")


class MenuItem(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    course = Column(Text)
    description = Column(Text)
    price = Column(String(50))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship('Restaurant')
    user_id = Column(Integer, ForeignKey('user.id'))


engine = create_engine('sqlite:///restaurantmenuwithusers.db')

Base.metadata.create_all(engine)
