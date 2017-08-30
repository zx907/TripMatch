from sqlalchemy.orm import sessionmaker
from tripmatch_model import Base,User, TripDetails
from sqlalchemy import create_engine

engine = create_engine('sqlite:///testdb.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

u1 = User(username='Alex', email='alex@gmail.com', password='123456')
u2 = User(username='Ben', email='ben@gmail.com', password='123456')
u3 = User(username='Claire', email='claire@gmail.com', password='123456')


t1 = TripDetails(username='Alex', country="US", date_start="20170706", companions=2)

session.add(u1)
session.commit()
session.add(u2)
session.commit()
session.add(u3)
session.commit()
session.add(t1)
session.commit()

for name in session.query(User).all():
    print(name.username)
