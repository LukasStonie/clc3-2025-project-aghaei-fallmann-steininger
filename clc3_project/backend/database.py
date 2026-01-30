import os
from sqlalchemy import create_engine

# This pulls the string you defined in docker-compose
DATABASE_URL = "postgresql://myadmin:MyComplexPassword123!@db:5432/postgres"#os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Create a Session class
# autocommit/flush=False is standard practice to prevent accidental writes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Create a Base class for your models to inherit from
Base = declarative_base()

# 3. Dependency to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()