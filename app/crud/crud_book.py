from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.Book import Book
from app.schemas.Book import BookUpdate, BookCreate
from app.validators.functions import validate_positive_int_numbers


def create_book(db: Session, data: BookCreate) -> Book:
    """
    Create a new book in the database.

    This function accepts database session and book creation data, then creates and
    stores a new book entry. If a book with the same title already exists, it raises
    an HTTPException signaling a conflict error.

    :param db: Database session used for performing ORM operations.
    :type db: Session
    :param data: Data required to create a new book, including title, author,
        category, price, and stock.
    :type data: BookCreate
    :return: Newly created book instance.
    :rtype: Book
    :raises HTTPException: Raises a conflict exception if a book with the same
        title already exists in the database.
    """
    existing_book = db.query(Book).filter(Book.title == data.title).first()
    if existing_book:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya existe")
    book = Book(
        title=data.title,
        author=data.author,
        category=data.category,
        price=data.price,
        stock=data.stock,
    )

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def read_books(db: Session, skip: int = 0, limit: int = 10) -> list:
    """
    Retrieves a list of non-deleted books from the database with pagination support. Ensures the
    pagination parameters are valid and raises appropriate HTTP exceptions in case of errors
    or if no books are found.

    :param db: Database session instance used to query the books
    :type db: Session
    :param skip: Number of entries to skip in the result set (used for pagination), must be positive
    :type skip: int
    :param limit: Maximum number of entries to return in the result set (used for pagination), must be positive
    :type limit: int
    :return: List of books retrieved from the database, empty list if no books are found
    :rtype: list
    :raises HTTPException: Raises a 400 error if ``skip`` or ``limit`` are not positive integers.
                           Raises a 404 error if no books are found.
                           Raises a 500 error for SQLAlchemy or other query-related exceptions.
    """
    if not validate_positive_int_numbers(skip, limit):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los valores de skip y limit deben ser positivos")

    try:
        books = db.query(Book).filter(Book.is_deleted == False).offset(skip).limit(limit).all()
    except SQLAlchemyError as db_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar los libros en la base de datos: {db_err}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar los libros: {e}"
        )
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro ningun libro")

    return books


def get_book(book_id, db, deleted=False) -> Book:
    """
    Retrieves a book from the database based on its ID. If the book is marked as
    deleted and the `deleted` parameter is not set to True, an exception is raised.
    Handles various exceptions to ensure robust error handling during the database
    query process.

    :param book_id: Unique identifier of the book to be retrieved.
    :type book_id: int
    :param db: Database session for querying the book information.
    :type db: Session
    :param deleted: Flag indicating whether to allow retrieval of deleted books.
                    Defaults to False.
    :type deleted: bool, optional
    :return: The book object corresponding to the given book ID.
    :rtype: Book
    :raises HTTPException: If an error occurs during the database query process.
    :raises HTTPException: If the book is not found in the database.
    :raises HTTPException: If the book is marked as deleted but `deleted` is False.
    :raises HTTPException: If the retrieved object is not of type Book.
    """
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar el libro: {e}"
        )
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro el libro")
    if book.is_deleted and not deleted:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El libro esta borrado")
    if not isinstance(book, Book):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El valor ingresado no es un libro")
    return book


def update_book(db: Session, book_id: int, update_data: BookUpdate) -> Book:
    """
    Update a book's information in the database dynamically using the provided update
    data. Any attributes not set in the update data will remain unchanged. The process
    includes committing database changes and refreshing the updated book instance.

    :param db: The database session used to interact with the database.
    :type db: Session
    :param book_id: The unique identifier of the book to update.
    :type book_id: int
    :param update_data: The data containing updates to be applied to the book.
    :type update_data: BookUpdate
    :return: The updated book instance after applying all changes, committing, and refreshing.
    :rtype: Book
    :raises HTTPException: If there is an error committing the changes to the database.
    """
    book = get_book(book_id, db)

    # Actualiza los datos dinamicamente
    for key, value in update_data.model_dump(exclude_unset=True).items():
        if hasattr(book, key):
            setattr(book, key, value)

    try:
        db.commit()
    except SQLAlchemyError as db_err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el libro en la base de datos: {db_err}"
        )
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> Book:
    """
    Deletes a book from the database by marking it as deleted. This operation modifies
    the `is_deleted` status of the book. If the book is already deleted, a conflict
    exception is raised.

    This function ensures that once a book is marked as deleted, it cannot be
    deleted again, preventing redundant operations.

    :param db: The database session used for querying and committing changes.
    :type db: Session
    :param book_id: The identifier of the book to be deleted.
    :type book_id: int
    :return: The updated book object with the `is_deleted` flag set to True.
    :rtype: Book
    :raises HTTPException: If the book is already marked as deleted.
    """
    book = get_book(book_id, db)

    if book.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El libro ya estaba borrado")

    book.is_deleted = True
    db.commit()
    db.refresh(book)
    return book


def restore_book(db: Session, book_id: int) -> Book:
    """
    Restores a previously deleted book by changing its `is_deleted` status to False
    and committing the update to the database. If the book is not marked as deleted,
    an HTTP 409 Conflict exception will be raised.

    :param db: Database session object used for querying and committing changes
    :param book_id: The unique identifier of the book to be restored
    :return: The restored book object
    :rtype: Book
    :raises HTTPException: Raised with status code HTTP_409_CONFLICT if the book
        is not marked as deleted
    """
    book = get_book(book_id, db, deleted=True)
    if not book.is_deleted:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="El libro no esta borrado")
    book.is_deleted = False
    db.commit()
    db.refresh(book)
    return book
