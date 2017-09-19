import unittest
import tripmatch
from tripmatch_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        # database engine and session
        engine = create_engine("sqlite:////testdb2.db")
        # create tables
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        tripmatch.trip_server.app.testing = True
        self.app = tripmatch.trip_server.app.test_client()

        with tripmatch.trip_server.app.app_context():
            tripmatch.trip_server.init_db()


    def tearDown(self):
        pass

    def test_login(self):
        rv = self.app.post('/register', data={'username':'tester', 'password':'123456'}, follow_redirects=True)
        assert b'You were logged in' in rv.data

    def test_logout(self):
        rv = self.app.get('/logout', follow_redirects=True)
        assert b'You were logged out' in rv.data


if __name__ == '__main__':
    unittest.main()