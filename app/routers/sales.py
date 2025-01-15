from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.functions import get_current_user, get_current_admin_user
from app.crud.crud_sale import create_sale, read_sales, delete_sale, read_user_sales
from app.database.config import get_db
from app.schemas.Sale import SaleCreate, SaleResponse

router = APIRouter()


@router.post("/", response_model=SaleResponse)
async def create_sale_route(sale: SaleCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Crea una nueva venta, el id del usuario se obtiene mediante el token JWT y se registra en la venta. Requiere permisos de usuario.
    """
    return create_sale(db=db, data=sale, user=current_user)


@router.get("/", response_model=List[SaleResponse])
async def read_sales_route(db: Session = Depends(get_db), admin=Depends(get_current_admin_user), skip: int = 0,
                           limit: int = 10):
    """
    Retorna las ventas en el intervalo skin:limit. Requiere permisos de administrador.
    """
    return read_sales(db=db, skip=skip, limit=limit)


@router.get("/user", response_model=List[SaleResponse])
async def read_user_sales_route(db: Session = Depends(get_db), user=Depends(get_current_user), skip: int = 0,
                                limit: int = 10):
    """
    Retorna las ventas del usuario logueado.
    """
    return read_user_sales(db, user.id, skip, limit)


@router.delete("/{sale_id}", response_model=SaleResponse)
async def delete_sale_route(sale_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin_user)):
    """
    Borra logicamente una venta de la base de datos. Requiere permisos de administrador.
    """
    return delete_sale(db=db, sale_id=sale_id)
