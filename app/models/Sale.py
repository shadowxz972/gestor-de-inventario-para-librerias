from datetime import date

from sqlalchemy import Column, Integer, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, validates

from app.database.config import Base
from app.validators.sale_validators import quantity_validation, total_price_validation, date_validation


class Sale(Base):
    """
    Represents the sales transactions in a bookstore system.

    The Sale class is an ORM model that maps to a "sales" table in the database. It records
    information about book sales, including the book and user associated with the sale,
    the quantity sold, the total price of the sale, and the date of the transaction.
    Additionally, it supports validation for specific attributes to ensure data integrity.

    :ivar id: Unique identifier for the sale record.
    :type id: int
    :ivar book_id: Foreign key referencing the book sold in the sale.
    :type book_id: int
    :ivar user_id: Foreign key referencing the user who made the purchase.
    :type user_id: int
    :ivar quantity: Number of items sold in the sale.
    :type quantity: int
    :ivar total_price: Calculated total price for the sale transaction.
    :type total_price: float
    :ivar date: Date of the sale transaction.
    :type date: datetime.date
    :ivar is_deleted: Soft delete flag indicating whether the sale record is deleted.
    :type is_deleted: bool
    :ivar book: ORM relationship to the associated Book object.
    :type book: sqlalchemy.orm.relationship
    :ivar user: ORM relationship to the associated User object.
    :type user: sqlalchemy.orm.relationship
    """
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Integer)
    total_price = Column(Float, default=0)
    date = Column(Date, default=date.today)
    is_deleted = Column(Boolean, default=False)

    book = relationship("Book", back_populates="sales", lazy="joined")

    user = relationship("User", back_populates="sales", lazy="joined")

    def __repr__(self):
        return f"<Sale(id={self.id}, book_id={self.book_id}, quantity={self.quantity}, total_price={self.total_price}, date={self.date})>"

    @validates("quantity")
    def validate_quantity(self, key, value: int):
        return quantity_validation(value)

    @validates("total_price")
    def validate_total_price(self, key, value: int):
        return total_price_validation(value)

    @validates("date")
    def validate_date(self, key, value: date):
        return date_validation(value)
