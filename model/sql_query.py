MODULATIONS = ("LTE", "WCDMA", "TDSCDMA", "CDMA2K")

def checkIfRecordExists(modulation, **kargs)
    if (session.query(UUT_TEST_INFO).filter_by(**filter_by_query).count() == 0):
        return False
    else:
        uut_id = session.query(UUT_TEST_INFO).filter_by(**filter_by_query).all()


    for mod in MODULATIONS:
        count = session.query(UUT_TEST_INFO, mod).filter(UUT_TEST_INFO.id==mod.uut_test_id)