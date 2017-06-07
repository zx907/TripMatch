from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymssql

from test_result_model import UUT_TEST_INFO, LTE_RESULT, WCDMA_RESULT, TDSCDMA_RESULT, CDMA2K_RESULT

engine = create_engine("mssql+pymssql://pash_user:123456789@10.105.56.131/TESTSTAND")

# conn = pymssql.connect("10.105.56.35", "pash_user", "1234536789", "TESTSTAND")
# cursor = conn.cursor()
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

filter_by_query = {'uut':'6440'}
s = session.query(UUT_TEST_INFO).filter_by(**filter_by_query).first()
print(s.serialize)



# for item in session.query(UUT_TEST_INFO):
#     print(item.serialize)