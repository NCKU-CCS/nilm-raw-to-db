import os
import sys
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Monitor(Base):
    __tablename__ = 'monitor'
    id = Column(String, primary_key=True)
    members_number = Column(Integer)
    architectural_area_m2 = Column(Integer, nullable=False)


class Estimation(Base):
    __tablename__ = 'estimation'
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    total_power = Column(Float, nullable=True)
    mac_address = Column(String(16))
    created_date = Column(DateTime)
    monitor = relationship('Monitor')
    monitor_id = Column(Integer, ForeignKey('monitor.id'))

    
class Appliance(Base):
    __tablename__ = 'appliance'
    id = Column(Integer, primary_key=True)
    appliance_id = Column(Integer)
    appliance_type_id = Column(Integer)
    appliance_name = Column(String(32))
    estimated_power = Column(Float)
    estimation = relationship('Estimation')
    estimation_id = Column(Integer, ForeignKey('estimation.id'))


class EnvironmentalSensor(Base):
    __tablename__ = 'environmental_sensor'
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    time = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Integer)
    co2_concentration = Column(Integer)
    sound_pressure = Column(Integer)
    air_pressure = Column(Float)
    monitor = relationship('Monitor')
    monitor_id = Column(Integer, ForeignKey('monitor.id'))

engine = create_engine('sqlite:///nilm.db')
Base.metadata.bind = engine
Base.metadata.create_all(engine)