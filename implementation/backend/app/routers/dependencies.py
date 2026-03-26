"""
routers/dependencies.py - Dependencias de FastAPI para inyección en endpoints.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.services.auth_service import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """
    Dependencia: decodifica el JWT e inyecta el usuario autenticado.
    Lanza HTTP 401 si el token es inválido o el usuario no existe.
    """
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodificar_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credenciales_exception
    except JWTError:
        raise credenciales_exception

    repo = UsuarioRepository(db)
    usuario = repo.get_by_email(email)
    if usuario is None or not usuario.activo:
        raise credenciales_exception
    return usuario


def require_admin(usuario: Usuario = Depends(get_usuario_actual)) -> Usuario:
    """Dependencia: verifica que el usuario tenga rol ADMIN."""
    if usuario.rol.value != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol ADMIN para esta operación.",
        )
    return usuario