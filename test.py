from database_setup import Restaurant, Base, MenuItem, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

res = session.query(Restaurant).filter_by(id=1).one()
print (res.name)
session.delete(res)
session.commit()

items = session.query(MenuItem).all()
for item in items:
	print (item.name)
	print (item.restaurant_id)
	print ('-------------------------------')

print ('*********************************')
restaurants = session.query(Restaurant).all()
for x in restaurants:
	print (x.name)
	print (x.id)
	print ('------------------------------')