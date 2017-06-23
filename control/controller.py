import pandas as pd
from sqlalchemy.sql import select, and_
from model.test_result_model import UUT_TEST_INFO, LTE_RESULT, WCDMA_RESULT, TDSCDMA_RESULT, CDMA2K_RESULT
import zipfile

def generateCsvFile(uut_test_id, modulation):
    EXCLUDE_KEYS = ('id' ,'execution_time', 'result_file', 'uut_test_id')

    files_to_download = []

    modulation = LTE_RESULT

    for _id in uut_test_id:
        for mod in modulation:
            data_select = select([UUT_TEST_INFO, mod]).where(and_(UUT_TEST_INFO.id==mod.uut_test_id, UUT_TEST_INFO.id==_id))
            df = pd.read_sql(data_select, project.engine)
            df.drop((key for key in EXCLUDE_KEYS), axis=1, inplace=True)
            filename = '{}_{}_{}.csv'.format(df.uut[0], mod.split('-')[0], df.start_date_time)
            df.to_csv('/files//' + filename)
            files_to_download.append(filename)

    with zipfile.ZipFile('/files/results.zip', 'w') as myzip:
        print('Zipping up files')
        myzip.write(f for f in files_to_download)