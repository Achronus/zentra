from app.config.settings import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(settings.DB.URL, connect_args=settings.DB.CONNECT_ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for retrieving a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
