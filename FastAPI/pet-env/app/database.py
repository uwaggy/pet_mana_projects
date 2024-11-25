from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL database connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:agnes@localhost/pet_man"

# Create the engine for PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()
