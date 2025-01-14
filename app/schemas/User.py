from typing import Optional

from pydantic import BaseModel, Field

from app.validators.constants import MAX_LENGTH_USER, MIN_LENGTH_USER, MIN_LENGTH_PASSWORD


class UserBase(BaseModel):
    username: str = Field(min_length=MIN_LENGTH_USER, max_length=MAX_LENGTH_USER)


class UserCreate(UserBase):
    password: str = Field(min_length=MIN_LENGTH_PASSWORD, max_length=MAX_LENGTH_USER)


class UserResponse(UserBase):
    id: int
    is_deleted: bool


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=MIN_LENGTH_USER, max_length=MAX_LENGTH_USER)
    password: Optional[str] = Field(None, min_length=MIN_LENGTH_PASSWORD)
