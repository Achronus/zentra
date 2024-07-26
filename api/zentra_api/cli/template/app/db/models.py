from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from . import Base, engine
from .crud import CRUD


class User(Base):
    """A model of the user table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


class DBConnections:
    """A place to store all table CRUD operations."""

    def __init__(self) -> None:
        self.user = CRUD(model=User)


CONNECT = DBConnections()
