"""
repositories/base_repository.py - Repositorio base genérico.

Patrón de Diseño: Repository
  - Abstrae el acceso a datos del resto de la aplicación.
  - Provee operaciones CRUD reutilizables para cualquier modelo.

Principio SOLID:
  - DIP: La capa de servicio depende de esta abstracción, no de SQLAlchemy directamente.
  - OCP: Abierto para extensión (subclases), cerrado para modificación.
"""
from typing import Generic, TypeVar, Type, Sequence
from sqlalchemy.orm import Session

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repositorio CRUD genérico. Todas las entidades heredan de esta clase
    para obtener las operaciones básicas de persistencia.
    """

    def __init__(self, model: Type[ModelType], db: Session) -> None:
        self.model = model
        self.db = db

    def get_by_id(self, record_id: int) -> ModelType | None:
        """Obtiene un registro por su clave primaria."""
        return self.db.get(self.model, record_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Obtiene todos los registros con paginación."""
        return (
            self.db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, instance: ModelType) -> ModelType:
        """Persiste una nueva instancia en la base de datos."""
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, instance: ModelType) -> ModelType:
        """Actualiza una instancia existente."""
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, record_id: int) -> bool:
        """Elimina un registro por su ID. Retorna True si fue encontrado y eliminado."""
        instance = self.get_by_id(record_id)
        if instance is None:
            return False
        self.db.delete(instance)
        self.db.commit()
        return True

    def count(self) -> int:
        """Retorna el número total de registros."""
        return self.db.query(self.model).count()