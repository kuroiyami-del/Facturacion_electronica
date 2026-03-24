"""
routers/auth.py - Endpoints de autenticación y registro.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.schemas import LoginRequest, TokenResponse, UsuarioCreate, UsuarioResponse
from app.services.auth_service import autenticar_usuario, crear_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Autentica al usuario y retorna un JWT de acceso."""
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crear_access_token(data={"sub": usuario.email, "rol": usuario.rol.value})
    return TokenResponse(access_token=token)


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en el sistema."""
    repo = UsuarioRepository(db)
    if repo.existe_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un usuario con el email {payload.email}.",
        )
    nuevo_usuario = Usuario(
        empresa_id=payload.empresa_id,
        nombre=payload.nombre,
        apellido=payload.apellido,
        email=payload.email,
        password_hash=hash_password(payload.password),
        rol=payload.rol,
    )
    return repo.create(nuevo_usuario)