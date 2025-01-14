from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.orm import validates, relationship

from app.database.config import Base
from app.validators.book_validators import title_validation, author_validation, category_validation, price_validation, \
    stock_validation


class Book(Base):
    """
    Represents a book entity in the database.

    This class is used to model the structure of the `books` table in the database.
    It includes information such as the title, author, category, price, stock, and
    whether the book is marked as deleted. It provides validation for its fields
    through the decorated methods to enforce proper data consistency.

    :ivar id: The unique identifier of the book.
    :type id: int
    :ivar title: The title of the book. It must be unique.
    :type title: str
    :ivar author: The author of the book.
    :type author: str
    :ivar category: The category or genre of the book.
    :type category: str
    :ivar price: The price of the book.
    :type price: float
    :ivar stock: The quantity of this book available in stock. Defaults to 0.
    :type stock: int
    :ivar is_deleted: Indicates whether the book is marked as deleted. Defaults to False.
    :type is_deleted: bool
    :ivar sales: The relationship with the Sale entity, defining the association
        between a book and its sales.
    :type sales: list[Sale]
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    author = Column(String)
    category = Column(String)
    price = Column(Float)
    stock = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False)

    sales = relationship("Sale", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', category='{self.category}', price={self.price}, stock={self.stock})>"

    @validates('title')
    def validate_title(self, key, value: str) -> str:
        return title_validation(value)

    @validates('author')
    def validate_author(self, key, value: str) -> str:
        return author_validation(value)

    @validates('category')
    def validate_category(self, key, value: str) -> str:
        return category_validation(value)

    @validates('price')
    def validate_price(self, key, value: float) -> float:
        return price_validation(value)

    @validates('stock')
    def validate_stock(self, key, value: int) -> int:
        return stock_validation(value)
