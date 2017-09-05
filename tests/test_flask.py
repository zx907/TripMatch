import unittest
import tripmatch
from tripmatch_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from tripmatch import create_app
# from tripmatch.trip_server import init_db

# def app(request):
#     config = {
#         'DATABSE': temp_db_location,
#         'TESTING': True
#     }

#     app = create_app(config=config)

#     with app.app_context():
#         init_db()
#         yield app




class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        # database engine and session
        engine = create_engine("sqlite:////testdb2.db")
        # create tables
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        


    def tearDown(self):
        

    def test_empty_db(self):
        pass


if __name__ == '__main__':
    unittest.main()