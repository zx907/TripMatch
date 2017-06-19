import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, and_
from model.test_result_model import UUT_TEST_INFO, LTE_RESULT, WCDMA_RESULT, TDSCDMA_RESULT, CDMA2K_RESULT
from project import engine, session

FILE_FILDER = '/files'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'txt'])

def generateCsvFile(uut_test_id, modulation):
    EXCLUDE_KEYS = ('id' ,'execution_time', 'result_file', 'uut_test_id')

    file_to_donwload = []

    for _id in uut_test_id:
        for mod in modulation:
            data_select = select([UUT_TEST_INFO, mod]).where(and_(UUT_TEST_INFO.id==mod.uut_test_id, UUT_TEST_INFO.id==_id))
            df = pd.read_sql(data_select, engine)
            df.drop((key for key in EXCLUDE_KEYS), axis=1, inplace=True)
            # export to a file name like uut_modulation_data.csv
            filename = "{0}_{1}_{2}.csv".format(df['uut'][0], mod.split('_')[0], df['start_date_time'][0])
            df.to_csv(filename)
            file_to_donwload.append(filename)