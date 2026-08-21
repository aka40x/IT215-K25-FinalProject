from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

def get_db():
    """Mở session database cho request và đóng session sau khi xử lý."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()