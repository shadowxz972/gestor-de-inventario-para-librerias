from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates, relationship

from app.database.config import Base
from app.validators.user_validators import username_validation, hashed_password_validation


class User(Base):
    """
    Represents a user in the application.

    This class defines the structure of a user, including their credentials, roles,
    and relationships with other database entities. It interacts with the database,
    validates input values for specific fields, and is used to manage user data
    within the application.

    :ivar id: Unique identifier for the user.
    :type id: int
    :ivar username: Unique username for the user.
    :type username: str
    :ivar hashed_password: Stored hashed password for the user.
    :type hashed_password: str
    :ivar is_admin: A flag indicating whether the user has administrative privileges.
    :type is_admin: bool
    :ivar is_deleted: A flag indicating whether the user account is marked as deleted.
    :type is_deleted: bool
    :ivar sales: A relationship to the Sale model representing sales associated with
        the user.
    :type sales: list[Sale]
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    sales = relationship("Sale", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, hashed_password={self.hashed_password})>"

    @validates("username")
    def validate_username(self, key, value: str) -> str:
        return username_validation(value)

    @validates("hashed_password")
    def validate_hashed_password(self, key, value: str) -> str:
        return hashed_password_validation(value)
