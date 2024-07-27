from typing import Any, Type
from sqlalchemy.orm import Session

from pydantic import BaseModel, ConfigDict


class CRUD(BaseModel):
    """
    Handles create, read, update, and delete operations for a database table.

    Parameters:
    - `model` (`db.Base`) - the database table to operate on. E.g., `db_models.Item`
    """

    model: Type

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get(self, db: Session, id: int) -> Any:
        """Utility method for getting a single item."""
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, data: dict) -> Any:
        """Adds an item to the table."""
        item = self.model(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get(self, db: Session, id: int) -> Any | None:
        """Retrieves a single item from the table."""
        return self._get(db, id)

    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100) -> list[Any]:
        """Retrieves multiple items from a table."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, id: int, data: BaseModel) -> Any | None:
        """Updates an item in the table."""
        result = self._get(db, id)

        if not result:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(result, field, value)

        db.commit()
        db.refresh(result)
        return result

    def delete(self, db: Session, id: int) -> Any | None:
        """Deletes an item from the table."""
        result = self._get(db, id)

        if result:
            db.delete(result)
            db.commit()

        return result


class UserCRUD(BaseModel):
    """
    Handles create, read, update, and delete operations for the `User` database table.

    Parameters:
    - `model` (`Base`) - the `User` database table to operate on
    """

    model: Type

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get(self, db: Session, attr: str, value: str) -> Any:
        """Utility method for getting a single user."""
        return db.query(self.model).filter(getattr(self.model, attr) == value).first()

    def create(self, db: Session, data: dict) -> Any:
        """Adds a user to the table."""
        item = self.model(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_by_username(self, db: Session, username: str) -> Any | None:
        """Retrieves a single user from the table by username."""
        return self._get(db, "username", username)

    def get_by_id(self, db: Session, id: int) -> Any | None:
        """Retrieves a single user from the table by ID."""
        return self._get(db, "id", id)

    def update(self, db: Session, id: int, data: BaseModel) -> Any | None:
        """Updates a users details in the table."""
        result = self._get(db, "id", id)

        if not result:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(result, field, value)

        db.commit()
        db.refresh(result)
        return result

    def delete(self, db: Session, id: int) -> Any | None:
        """Deletes an item from the table."""
        result = self._get(db, "id", id)

        if result:
            db.delete(result)
            db.commit()

        return result
