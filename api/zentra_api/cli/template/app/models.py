"""Contains all SQL database models and CRUD connections."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .config import SETTINGS
from zentra_api.crud import CRUD, UserCRUD


class User(SETTINGS.SQL.Base):
    """A model of the `User` table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class UserDetails(SETTINGS.SQL.Base):
    """A model of the `UserDetails` table."""

    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    full_name = Column(String)


SETTINGS.SQL.create_all()


class DBConnections:
    """A place to store all table CRUD operations."""

    def __init__(self) -> None:
        self.user = UserCRUD(model=User)
        self.user_details = CRUD(model=UserDetails)


CONNECT = DBConnections()
