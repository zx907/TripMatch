from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymssql
import pandas as pd
from sqlalchemy.sql import select, and_

from test_result_model import UUT_TEST_INFO, LTE_RESULT, WCDMA_RESULT, TDSCDMA_RESULT, CDMA2K_RESULT

engine = create_engine(
    "mssql+pymssql://pash_user:123456789@10.105.56.131/TESTSTAND")

# conn = pymssql.connect("10.105.56.35", "pash_user", "1234536789", "TESTSTAND")
# cursor = conn.cursor()
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

# l = [LTE_RESULT]

# filter_by_query = {'uut': '6440'}
# s = session.query(UUT_TEST_INFO).filter_by(**filter_by_query).first()
# mod = 'LTE_RESULT'
# q = session.query(UUT_TEST_INFO, LTE_RESULT).filter(UUT_TEST_INFO.id==LTE_RESULT.uut_test_id).filter(UUT_TEST_INFO.uut=="6440").first()
# c = session.query(UUT_TEST_INFO, l[0]).filter(UUT_TEST_INFO.id==LTE_RESULT.uut_test_id).filter(UUT_TEST_INFO.uut=="6440").count()

# data_select = select(UUT_TEST_INFO, LTE_RESULT).filter(UUT_TEST_INFO.id==LTE_RESULT.uut_test_id).filter(UUT_TEST_INFO.id==102)
mod = LTE_RESULT
data_select = select([UUT_TEST_INFO, mod]).where(and_(UUT_TEST_INFO.id==mod.uut_test_id, UUT_TEST_INFO.id==112))
df = pd.read_sql(data_select, engine)
print(df.columns)
EXCLUDE_KEYS = ('id' ,'execution_time', 'result_file', 'uut_test_id')
df.drop((key for key in EXCLUDE_KEYS), axis=1, inplace=True)
print(df.columns)

# print(q[1].serialize)


# for item in session.query(UUT_TEST_INFO):
#     print(item.serialize)
