"""
repositories/usuario_repository.py - Acceso a datos para la entidad Usuario.
Principio SRP: Solo gestiona operaciones de persistencia de usuarios.
"""
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    """
    Repositorio especializado para la entidad Usuario.
    Extiende el CRUD base con consultas específicas del dominio.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(Usuario, db)

    def get_by_email(self, email: str) -> Usuario | None:
        """Busca un usuario por su dirección de email (único en el sistema)."""
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

    def get_activos_por_empresa(self, empresa_id: int) -> list[Usuario]:
        """Retorna todos los usuarios activos de una empresa específica."""
        return (
            self.db.query(Usuario)
            .filter(
                Usuario.empresa_id == empresa_id,
                Usuario.activo == True,
            )
            .all()
        )

    def existe_email(self, email: str) -> bool:
        """Verifica si ya existe un usuario registrado con ese email."""
        return (
            self.db.query(Usuario.id)
            .filter(Usuario.email == email)
            .first()
            is not None
        )

    def desactivar(self, usuario_id: int) -> Usuario | None:
        """Desactiva un usuario sin eliminarlo (soft delete)."""
        usuario = self.get_by_id(usuario_id)
        if usuario:
            usuario.activo = False
            self.db.commit()
            self.db.refresh(usuario)
        return usuario