import unittest
import tripmatch

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        tripmatch.app.testing = True
        self.app = tripmatch.app.test_client()
        with tripmatch.app.app_context():
            tripmatch.init_db()


    def tearDown(self):
        pass

    def test_empty_db(self):
        pass


if __name__ == '__main__':
    unittest.main()