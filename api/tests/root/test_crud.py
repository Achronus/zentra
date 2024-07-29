import pytest

from zentra_api.crud import CRUD, UserCRUD

from sqlalchemy import create_engine, Column, Integer, String, StaticPool
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase
from pydantic import BaseModel

Base: DeclarativeBase = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


class TestCRUD:
    @pytest.fixture
    def item_crud(self):
        return CRUD(model=Item)

    @staticmethod
    def test_create_item(test_db, item_crud: CRUD):
        data = {"name": "Test Item"}
        item = item_crud.create(test_db, data)
        assert item.name == data["name"]
        assert item.id is not None

    @staticmethod
    def test_get_item(test_db, item_crud: CRUD):
        data = {"name": "Test Item"}
        item = item_crud.create(test_db, data)
        retrieved_item = item_crud.get(test_db, item.id)
        assert retrieved_item.id == item.id
        assert retrieved_item.name == item.name

    @staticmethod
    def test_get_multiple_items(test_db, item_crud: CRUD):
        data1 = {"name": "Test Item 1"}
        data2 = {"name": "Test Item 2"}
        item_crud.create(test_db, data1)
        item_crud.create(test_db, data2)
        items = item_crud.get_multiple(test_db)
        assert len(items) == 2

    @staticmethod
    def test_update_item(test_db, item_crud: CRUD):
        class ItemCreate(BaseModel):
            name: str

        data = {"name": "Test Item"}
        item = item_crud.create(test_db, data)
        update_data = ItemCreate(name="Updated Item")
        updated_item = item_crud.update(test_db, item.id, update_data)
        assert updated_item.name == update_data.name

    @staticmethod
    def test_update_result_none(test_db, item_crud: CRUD):
        class ItemCreate(BaseModel):
            name: str

        non_existent_id = 9999
        update_data = ItemCreate(name="Updated Item")
        result = item_crud.update(test_db, non_existent_id, update_data)
        assert result is None

    @staticmethod
    def test_delete_item(test_db, item_crud: CRUD):
        data = {"name": "Test Item"}
        item = item_crud.create(test_db, data)
        item_crud.delete(test_db, item.id)
        assert item_crud.get(test_db, item.id) is None


class TestUserCRUD:
    @pytest.fixture
    def user_crud(self):
        return UserCRUD(model=User)

    @staticmethod
    def test_create(test_db, user_crud: UserCRUD):
        data = {"username": "testUser", "password": "testpassword"}
        user = user_crud.create(test_db, data)
        assert user.username == data["username"]
        assert user.password == data["password"]
        assert user.id is not None

    @staticmethod
    def test_get_by_username(test_db, user_crud: UserCRUD):
        data = {"username": "testUser", "password": "testpassword"}
        user = user_crud.create(test_db, data)
        retrieved_user = user_crud.get_by_username(test_db, user.username)
        assert retrieved_user.id == user.id
        assert retrieved_user.username == user.username

    @staticmethod
    def test_get_by_id(test_db, user_crud: UserCRUD):
        data = {"username": "testUser", "password": "testpassword"}
        user = user_crud.create(test_db, data)
        retrieved_user = user_crud.get_by_id(test_db, user.id)
        assert retrieved_user.id == user.id
        assert retrieved_user.username == user.username

    @staticmethod
    def test_update(test_db, user_crud: UserCRUD):
        class UserCreate(BaseModel):
            username: str
            password: str

        data = {"username": "testUser", "password": "testpassword"}
        user = user_crud.create(test_db, data)
        update_data = UserCreate(username="newUser", password="newpassword")
        updated_user = user_crud.update(test_db, user.id, update_data)
        assert updated_user.username == update_data.username

    @staticmethod
    def test_update_result_none(test_db, user_crud: UserCRUD):
        class UserCreate(BaseModel):
            username: str
            password: str

        non_existent_id = 9999
        update_data = UserCreate(username="newUser", password="newpassword")
        result = user_crud.update(test_db, non_existent_id, update_data)
        assert result is None

    @staticmethod
    def test_delete(test_db, user_crud: UserCRUD):
        data = {"username": "testUser", "password": "testpassword"}
        user = user_crud.create(test_db, data)
        user_crud.delete(test_db, user.id)
        assert user_crud.get_by_id(test_db, user.id) is None
