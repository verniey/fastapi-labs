from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/task1"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
