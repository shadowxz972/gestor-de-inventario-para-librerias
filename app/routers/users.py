from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.functions import get_current_admin_user, get_current_user
from app.crud.crud_user import delete_user, create_admin_user, restore_user, change_password
from app.database.config import get_db
from app.schemas.User import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.delete("/delete/{user_id}", response_model=UserResponse)
async def delete_user_route(user_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin_user)):
    """
    Borra logicamente a un usuario de la base de datos, requiere permisos de admin
    """
    return delete_user(db, user_id)


@router.delete("/delete_me", response_model=UserResponse)
async def delete_me_route(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Borra logicamente la cuenta del usuario que inicio sesion, requiere permisos de usuario
    """
    return delete_user(db, current_user.id)


@router.post("/create", response_model=UserResponse)
async def create_admin_user_route(data: UserCreate, db: Session = Depends(get_db),
                                  admin=Depends(get_current_admin_user)):
    """
    Crea un usuario administrador en la base de datos. Requiere permisos de admin
    """
    return create_admin_user(db, data)


@router.get("/restore/{user_id}", response_model=UserResponse)
async def restore_user_route(user_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin_user)):
    """
    Restaura a un usuario de la base de datos. requiere permisos de admin
    """
    return restore_user(db, user_id)


@router.put("/change_password", response_model=UserResponse)
async def change_password_route(new_password: UserUpdate, user=Depends(get_current_user),
                                db: Session = Depends(get_db)):
    """
    Cambia la contraseña del usuario logueado. requiere permisos de usuario
    """
    return change_password(db, user.id, new_password.password)
