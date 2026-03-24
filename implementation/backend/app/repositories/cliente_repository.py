"""
repositories/cliente_repository.py - Acceso a datos para la entidad Cliente.
"""
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):
    """Repositorio especializado para la entidad Cliente."""

    def __init__(self, db: Session) -> None:
        super().__init__(Cliente, db)

    def get_by_documento(self, numero_documento: str) -> Cliente | None:
        """Busca un cliente por su número de documento de identidad."""
        return (
            self.db.query(Cliente)
            .filter(Cliente.numero_documento == numero_documento)
            .first()
        )

    def buscar_por_nombre(self, texto: str) -> list[Cliente]:
        """Búsqueda de clientes por nombre (insensible a mayúsculas)."""
        patron = f"%{texto.lower()}%"
        return (
            self.db.query(Cliente)
            .filter(Cliente.nombre.ilike(patron))
            .all()
        )

    def get_activos(self, skip: int = 0, limit: int = 100) -> list[Cliente]:
        """Retorna solo los clientes activos."""
        return (
            self.db.query(Cliente)
            .filter(Cliente.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def existe_documento(self, numero_documento: str) -> bool:
        """Verifica si ya existe un cliente con ese número de documento."""
        return (
            self.db.query(Cliente.id)
            .filter(Cliente.numero_documento == numero_documento)
            .first()
            is not None
        )