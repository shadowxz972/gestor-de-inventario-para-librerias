from datetime import date

from pydantic import BaseModel


class SaleModel(BaseModel):
    book_id: int
    quantity: int
    date: date


class SaleCreate(SaleModel):
    pass


class SaleResponse(SaleModel):
    id: int
    total_price: float
    is_deleted: bool
    user_id: int
