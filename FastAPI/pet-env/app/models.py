from sqlalchemy import Column, Integer, String
from .database import Base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String, index=True)
    age = Column(Integer)
