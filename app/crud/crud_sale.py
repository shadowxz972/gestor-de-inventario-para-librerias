from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.Book import Book
from app.models.Sale import Sale
from app.models.User import User
from app.schemas.Sale import SaleCreate
from app.validators.functions import validate_positive_int_numbers

def fetch_sales(db: Session, filters: list, skip: int = 0, limit: int = 10):
    if not validate_positive_int_numbers(skip, limit):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los valores de skip y limit deben ser positivos"
        )
    result = db.query(Sale).filter(*filters).offset(skip).limit(limit).all()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron resultados"
        )
    return result


def create_sale(db: Session, data: SaleCreate, user: User):
    """
    Creates a new sale record in the database for a specific book and user.

    This function facilitates the creation of a sale by validating the existence of the book,
    checking that the book is not deleted, and ensuring the requested quantity does
    not exceed the current stock of the book. It calculates the total price of the sale,
    updates the book stock, and creates a corresponding sale record in the database.

    :param db: Database session used to interact with the database
    :type db: Session
    :param data: Data regarding the sale, including book ID, quantity, and sale date
    :type data: SaleCreate
    :param user: User entity initiating the sale
    :type user: User
    :return: The newly created Sale object
    :rtype: Sale
    :raises HTTPException: If the specified book does not exist
    :raises HTTPException: If the specified book is marked as deleted
    :raises HTTPException: If the requested sale quantity exceeds available stock
    """
    book = db.query(Book).filter(Book.id == data.book_id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro especificado no existe")

    if book.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro esta borrado")

    if data.quantity > book.stock:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="La cantidad de la venta excede a la cantidad de libros")

    total_price = book.price * data.quantity
    book.stock -= data.quantity
    new_sale = Sale(
        book_id=data.book_id,
        quantity=data.quantity,
        date=data.date,
        user_id=user.id,
    )

    new_sale.total_price = total_price

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    db.refresh(book)
    return new_sale


def read_sales(db: Session, skip: int = 0, limit: int = 10):
    """
    Reads sales data from the database with an optional ability to skip a certain
    number of records and limit the size of the result set. The function ensures
    that only non-deleted sales records are fetched by applying a filter.

    :param db: A SQLAlchemy session object used to perform database operations.
    :param skip: Number of sales records to skip. Default value is 0.
    :param limit: Maximum number of sales records to retrieve. Default value is 10.
    :return: A list of sales records retrieved from the database.
    """
    filters = [Sale.is_deleted == False]
    return fetch_sales(db, filters, skip, limit)


def read_user_sales(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """
    Fetches sales data for a specific user with optional pagination.

    This function retrieves a list of sales records associated with a particular
    user ID by querying the database. The results can be paginated using the
    `skip` and `limit` parameters. Only records marked as not deleted are
    returned.

    :param db: Database session used for querying.
    :type db: Session
    :param user_id: Unique identifier for the user whose sales data is to be fetched.
    :type user_id: int
    :param skip: The number of records to skip before starting to fetch results. Defaults to 0.
    :type skip: int
    :param limit: The maximum number of records to retrieve. Defaults to 10.
    :type limit: int
    :return: A list of sales records for the given user.
    :rtype: List[Sale]
    """
    filters = [Sale.is_deleted == False, Sale.user_id == user_id]
    return fetch_sales(db, filters, skip, limit)

def delete_sale(db: Session, sale_id: int):
    """
    Marks a sale record in the database as deleted by setting its `is_deleted` flag
    to `True`. This function first checks if the sale record exists and whether it
    has already been marked as deleted. If the record does not exist or is already
    deleted, appropriate HTTP exceptions are raised.

    :param db: Database session used to query and update the sale record
    :param sale_id: ID of the sale record to be marked as deleted
    :return: The updated sale record with the `is_deleted` flag set to `True`
    :rtype: Sale
    :raises HTTPException: Raised with status 404 if the sale record is not found
    :raises HTTPException: Raised with status 409 if the sale record is already
        marked as deleted
    """
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro el libro")

    if sale.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El libro ya estaba borrado")

    sale.is_deleted = True
    db.commit()
    db.refresh(sale)
    return sale

def restore_sale():
    pass