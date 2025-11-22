from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from .config import settings

# Esquema simple "Bearer" para Swagger y para los endpoints
bearer_scheme = HTTPBearer()


# Usuario de prueba en memoria. En un caso real iría a BD / Firebase.
FAKE_USER_DB = {
    "admin": {
        "username": "admin",
        "password": "admin",  # Plain-text solo para la prueba
    }
}

def authenticate_user(username: str, password: str) -> bool:
    user = FAKE_USER_DB.get(username)
    if not user:
        return False
    return user["password"] == password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un JWT propio del microservicio.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Dict[str, Any]:
    """
    Valida el JWT enviado en Authorization: Bearer <token>.
    Devuelve el payload decodificado si es válido.
    """
    token = credentials.credentials  # solo el token, sin "Bearer "

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise credentials_exception

    sub = payload.get("sub")
    if sub is None:
        raise credentials_exception

    # IMPORTANTE: NO verificar aquí en FAKE_USER_DB, para permitir uid de Firebase, etc.
    return payload