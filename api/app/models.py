from sqlalchemy import Column, Integer, BigInteger, Float, Date, String
from .database import Base

class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(BigInteger, nullable=False, index=True)
    campaign_id = Column(BigInteger, nullable=False, index=True)
    cost_micros = Column(BigInteger, nullable=False)
    clicks = Column(Float, nullable=False)
    conversions = Column(Float, nullable=False)
    impressions = Column(Float, nullable=False)
    interactions = Column(Float, nullable=False)
    date = Column(Date, nullable=False, index=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False) 
    role = Column(String, nullable=False)
