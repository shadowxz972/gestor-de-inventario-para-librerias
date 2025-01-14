from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Configuración de encriptacion y autenticacion
SECRET_KEY = "h55$?)a=2iuLG~HUAOfw8G(^}D?+<u"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Instancia para manejar el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema para extraer el token desde el cliente
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
