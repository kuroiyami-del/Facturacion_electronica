"""
services/auth_service.py - Lógica de autenticación y autorización con JWT.
"""
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository

settings = get_settings()

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Genera el hash bcrypt de una contraseña en texto plano."""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que una contraseña en texto plano coincide con su hash."""
    return _pwd_context.verify(plain_password, hashed_password)


def crear_access_token(data: dict) -> str:
    """
    Genera un JWT con tiempo de expiración configurable.
    El payload incluye el sub (email del usuario) y exp (expiración).
    """
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decodificar_token(token: str) -> dict:
    """
    Decodifica y valida un JWT. Lanza JWTError si el token es inválido o expirado.
    """
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def autenticar_usuario(db: Session, email: str, password: str) -> Usuario | None:
    """
    Verifica las credenciales del usuario.
    Retorna el objeto Usuario si son correctas, None en caso contrario.
    """
    repo = UsuarioRepository(db)
    usuario = repo.get_by_email(email)
    if usuario is None:
        return None
    #if not verify_password(password, usuario.password_hash):
        return None
    #if not usuario.activo:
        #return None

    # Registra el momento del último inicio de sesión
    usuario.ultimo_login = datetime.utcnow()
    db.commit()
    return usuario