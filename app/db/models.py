from sqlalchemy import Column, String, Integer, BigInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class State(Base):
    __tablename__ = "state"
    __table_args__ = {"schema": "public"}

    code = Column(String(2), primary_key=True)
    name = Column(String(20), nullable=False)
    country = Column(String(20), nullable=False)

class Attorney(Base):
    __tablename__ = "attorney"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    jurisdiction = Column(String(2), nullable=False)
    source = Column(String(200))
    name = Column(String(100), nullable=False)
    bar = Column(Integer)
    phone = Column(String(20))
    address = Column(String(400))
    date_admitted = Column(TIMESTAMP)
    law_school = Column(String(100))
    license_status = Column(String(20))
    rating = Column(String(100))
