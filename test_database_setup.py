from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Restaurant , Course

from sqlalchemy.sql import exists

engine = create_engine('sqlite:///restaurant.db')

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)

session = DBSession()

C_1 = Restaurant(name='1st_restaurant')
C_2 = Restaurant(name='2nd_restaurant')
C_3 = Restaurant(name='3rd_restaurant')

SC_11 = Course(name='London', restaurant_id='1')
SC_12 = Course(name='Paris', restaurant_id='1')
SC_21 = Course(name='Water', restaurant_id='2')
SC_22 = Course(name='Earth', restaurant_id='2')
SC_31= Course(name='Panda', restaurant_id='3')
SC_32 = Course(name='Tiger', restaurant_id='3')

session.add(C_1)
session.commit()
session.add(C_2)
session.commit()
session.add(C_3)
session.commit()
session.add(SC_11)
session.commit()
session.add(SC_12)
session.commit()
session.add(SC_21)
session.commit()
session.add(SC_22)
session.commit()
session.add(SC_31)
session.commit()
session.add(SC_32)
session.commit()

print ('commit all info')

print('############################')

for course in session.query(Restaurant):
    print((course.name))
print('----------------------------')
for course in session.query(Course):
    print((course.name, course.id, course.restaurant_id))

print('-----------------------------')
a = session.query(Course).filter_by(restaurant_id=2).all()
for b in a:
    print((b.name, b.description))
# session.query(Course).filter_by(name='Water').update({'description':'no more words'})
# session.commit()
print('all done')

print('-----------------------------')
current_restaurant_id = session.query(Restaurant).filter_by(name='2nd_restaurant').one().id
print(current_restaurant_id)

print('-----------------------------')
current_restaurant_id = session.query(Restaurant).filter_by(name='1st_restaurant').one().id
print(current_restaurant_id)
courses = session.query(Course).filter_by(restaurant_id=current_restaurant_id).all()
for x in courses:
    print(x.name, x.description)
