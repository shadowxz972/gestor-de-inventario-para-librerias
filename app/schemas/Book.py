from typing import Optional

from pydantic import BaseModel, Field

from app.validators.constants import MAX_LENGTH_TITLE


class BookBase(BaseModel):
    title: str
    author: str
    category: str
    price: float
    stock: int


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    is_deleted: bool


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=MAX_LENGTH_TITLE)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
