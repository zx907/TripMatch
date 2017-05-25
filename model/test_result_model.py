from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime

Base = declarative_base()

class UUT_TEST_INFO(Base):
    __tablename__= 'UUT_TEST_INFO'
    id = Column(Integer, primary_key=True)
    uut = Column(String(255), nullable=True)
    uut_serial_number = Column(String(255), nullable=True)
    start_date_time = Column(DateTime, nullable=True)
    notes = Column(String(1024), nullable=True)
    temperature = Column(Float, nullable=True)

    lte_result = relationship("LTE_RESULT")
    wcdma_result = relationship("WCDMA_RESULT")
    tdscdma_result = relationship("TDSCDMA_RESULT")
    cdma2k_result = relationship("CDMA2K_RESULT")

class TEST_RESULT_BASE(): 
    freq = Column(Float, nullable=True)
    vbatt_voltage = Column(Float, nullable=True)
    vbatt_current = Column(Float, nullable=True)
    vbatt_power = Column(Float, nullable=True)
    vcc_voltage = Column(Float, nullable=True)
    vcc_current = Column(Float, nullable=True)
    vcc_power = Column(Float, nullable=True)
    pae = Column(Float, nullable=True)
    pout = Column(Float, nullable=True)
    pin = Column(Float, nullable=True)
    gain = Column(Float, nullable=True)
    dc_power = Column(Float, nullable=True)
    ch_power = Column(Float, nullable=True)
    utra_lowadj = Column(Float, nullable=True)
    utra_highadj = Column(Float, nullable=True)
    utra_lowalt = Column(Float, nullable=True)
    utra_highalt = Column(Float, nullable=True)
    rms_mean = Column(Float, nullable=True)
    rms_max = Column(Float, nullable=True)
    freq_error_mean = Column(Float, nullable=True)
    target_power = Column(Float, nullable=True)
    vcc = Column(Float, nullable=True)
    vbatt = Column(Float, nullable=True)
    waveform = Column(String(50), nullable=True)
    mipi = Column(String(255), nullable=True)

class LTE_RESULT(Base, TEST_RESULT_BASE):
    __tablename__ = "LTE_RESULT"
    id = Column(Integer, primary_key=True)
    uut_test_id = Column(Integer, ForeignKey('UUT_TEST_INFO.id'))
    eutra_low = Column(Float, nullable=True)
    eutra_high = Column(Float, nullable=True)

class WCDMA_RESULT(Base, TEST_RESULT_BASE):
    __tablename__ = "WCDMA_RESULT"
    id = Column(Integer, primary_key=True)
    uut_test_id = Column(Integer, ForeignKey('UUT_TEST_INFO.id'))
    chip_rate_error = Column(Float, nullable=True)

class TDSCDMA_RESULT(Base, TEST_RESULT_BASE):
    __tablename__ = "TDSCDMA_RESULT"
    id = Column(Integer, primary_key=True)
    uut_test_id = Column(Integer, ForeignKey('UUT_TEST_INFO.id'))
    chip_rate_error = Column(Float, nullable=True)
    
class CDMA2K_RESULT(Base, TEST_RESULT_BASE):
    __tablename__ = "CDMA2K_RESULT"
    id = Column(Integer, primary_key=True)
    uut_test_id = Column(Integer, ForeignKey('UUT_TEST_INFO.id'))
    chip_rate_error = Column(Float, nullable=True)
