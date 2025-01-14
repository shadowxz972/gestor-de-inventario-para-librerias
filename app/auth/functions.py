from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.auth.config import pwd_context, SECRET_KEY, ALGORITHM, oauth2_scheme
from app.database.config import get_db
from app.models.User import User


# Funciones para manejar contraseñas
def hash_password(password: str) -> str:
    """
    Hashea la contraseña
    :param password:
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_token(token: str) -> dict:
    """
    Verifica el token JWT
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def create_access_token(user: User):
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {
        "sub": str(user.id),
        "is_admin": user.is_admin,
        "exp": expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se ha podido validar las credenciales",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise credentials_exception
    if not isinstance(user, User):
        raise credentials_exception
    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario esta eliminado"
        )

    return user


def get_current_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(token,db)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos para hacer esta accion"
        )
    return user
