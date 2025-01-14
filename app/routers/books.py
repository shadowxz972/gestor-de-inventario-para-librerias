from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.functions import get_current_admin_user, get_current_user
from app.crud.crud_book import read_books, create_book, update_book, delete_book, get_book, restore_book
from app.database.config import get_db
from app.schemas.Book import BookResponse, BookCreate, BookUpdate

router = APIRouter()


@router.post("/", response_model=BookResponse)
async def create_book_route(book: BookCreate, db: Session = Depends(get_db), admin = Depends(get_current_admin_user)):
    """
    Crea un libro y lo añade a la base de datos. Requiere permisos de administrador.
    """
    return create_book(db=db, data=book)


@router.get("/", response_model=List[BookResponse])
async def read_books_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Retorna los libros en el intervalo skin:limit. Requiere permisos de usuario.
    """
    return read_books(db, skip=skip, limit=limit)

@router.get("/{book_id}", response_model=BookResponse)
async def read_book_route(book_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Retorna un libro por su id. Requiere permisos de usuario.
    """
    return get_book(book_id, db)


@router.put("/", response_model=BookResponse)
async def update_book_route(book_id: int, book: BookUpdate, db: Session = Depends(get_db), admin = Depends(get_current_admin_user)):
    """
    Actualiza los datos de un libro. Requiere permisos de administrador.
    """
    return update_book(db=db, book_id=book_id, update_data=book)


@router.delete("/{book_id}", response_model=BookResponse)
async def delete_book_route(book_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin_user)):
    """
    Borra logicamente un libro de la base de datos. Requiere permisos de administrador.
    """
    return delete_book(book_id=book_id, db=db)

@router.get("/restore/{book_id}", response_model=BookResponse)
async def restore_book_route(book_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin_user)):
    """
    Recupera logicamente a un libro de la base de datos. Requiere permisos de administrador.
    """
    return restore_book(db,book_id)