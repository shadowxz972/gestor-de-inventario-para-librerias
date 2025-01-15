from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.functions import create_access_token, verify_password
from app.crud.crud_user import create_user
from app.database.config import get_db
from app.models.User import User
from app.schemas.LoginForm import LoginForm
from app.schemas.Token import Token
from app.schemas.User import UserResponse, UserCreate

router = APIRouter()


def login(db, user_credentials):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario esta eliminado"
        )
    access_token = create_access_token(user)
    return access_token


@router.post("/login", response_model=Token)
async def login_route(user_credentials: LoginForm, db: Session = Depends(get_db)):
    """
    Retorna un token JWT para el usuario si inicia sesion correctamente.
    """
    access_token = login(db, user_credentials)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register_route(user_credentials: UserCreate, db: Session = Depends(get_db)):
    """
    Registra a un nuevo usuario en la base de datos.
    """
    return create_user(db=db, data=user_credentials)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Este endpoint es para poder usar las rutas protegidas desde el swagger
    """
    access_token = login(db, form_data)
    return {"access_token": access_token, "token_type": "bearer"}
