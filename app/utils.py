from app.crud.crud_user import create_admin_user
from app.database.config import SessionLocal
from app.models.User import User
from app.schemas.User import UserCreate


def default_admin():
    db = SessionLocal()
    existing_admin = db.query(User).filter(User.is_admin).first()
    if not existing_admin:
        default_info = UserCreate(
            username="admin",
            password="contraseña",
        )
        create_admin_user(db, default_info)
