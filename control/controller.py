import numpy as np
import pandas as pd
import project as prj

def generateCsvFile(uut_test_id, modulation):
    EXCLUDE_KEYS = ('id' ,'execution_time', 'result_file', 'uut_test_id')

    for _id in uut_test_id:
        for mod in modulation:
            data_select = select([UUT_TEST_INFO, mod]).where(and_(UUT_TEST_INFO.id==mod.uut_test_id, UUT_TEST_INFO.id==_id))
            df = pd.read_sql(data, engine)
            df.drop((key for key in EXCLUDE_KEYS), axis=1, inplace=True)
            df.to_csv('%s_%s_%s.csv'.format(df.uut[0], mod.split('-')[0], df.start_date_time))