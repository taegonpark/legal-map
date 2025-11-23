from sqlalchemy import Column, String, Integer, BigInteger, TIMESTAMP, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class DetailTypeEnum(Base):
    __tablename__ = "detail_type_enum"
    __table_args__ = {"schema": "public"}

    detail_type = Column(String(100), primary_key=True)

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
    jurisdiction = Column(String(2), ForeignKey("public.state.code"), nullable=False)
    source = Column(String(200))
    name = Column(String(100), nullable=False)
    bar = Column(Integer)
    phone = Column(String(20))
    address = Column(String(400))
    date_admitted = Column(TIMESTAMP)
    law_school = Column(String(100))
    license_status = Column(String(20))
    rating = Column(String(100))

    details = relationship("AttorneyDetail", back_populates="attorney")  # relationship for convenience

class AttorneyDetail(Base):
    __tablename__ = "attorney_detail"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    attorney_id = Column(BigInteger, ForeignKey("public.attorney.id"), nullable=False)
    detail_type = Column(String(100), ForeignKey("public.detail_type_enum.detail_type"), nullable=False)
    detail = Column(Text, nullable=False)

    attorney = relationship("Attorney", back_populates="details")

