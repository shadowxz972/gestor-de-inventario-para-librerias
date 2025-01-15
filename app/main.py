import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import configure_mappers

from app.database.config import Base, engine
from app.routers.auth import router as auth_router
from app.routers.books import router as books_router
from app.routers.sales import router as sales_router
from app.routers.users import router as users_router
from app.utils import default_admin

configure_mappers()
Base.metadata.create_all(bind=engine)
default_admin()
app = FastAPI(
    title="Gestor de inventario para librerias",
    summary="""
    Con esta api podras gestionar el inventario de libros y las ventas.
    Tambien, incluye con gestion de usuarios.
    """
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(sales_router, prefix="/sales", tags=["sales"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Bienvenido al gestor de inventario para librerias"}


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
    )
