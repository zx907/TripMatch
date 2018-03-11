from sqlalchemy.orm import sessionmaker
from db.tripmatch_model import Base, Users, TripDetails
from sqlalchemy import create_engine

engine = create_engine('sqlite:///testdb.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

for t, u in session.query(TripDetails, Users).filter(Users.id==1).all():
    print(t)
    print(u)
