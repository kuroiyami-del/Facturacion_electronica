"""
repositories/producto_repository.py - Acceso a datos para la entidad Producto.
"""
from sqlalchemy.orm import Session

from app.models.producto import Producto
from app.repositories.base_repository import BaseRepository


class ProductoRepository(BaseRepository[Producto]):
    """Repositorio especializado para la entidad Producto."""

    def __init__(self, db: Session) -> None:
        super().__init__(Producto, db)

    def get_by_codigo(self, codigo: str) -> Producto | None:
        """Busca un producto por su código único."""
        return (
            self.db.query(Producto)
            .filter(Producto.codigo == codigo)
            .first()
        )

    def get_activos(self, skip: int = 0, limit: int = 100) -> list[Producto]:
        """Retorna solo los productos activos en el catálogo."""
        return (
            self.db.query(Producto)
            .filter(Producto.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def buscar_por_nombre(self, texto: str) -> list[Producto]:
        """Búsqueda de productos por nombre (insensible a mayúsculas)."""
        patron = f"%{texto.lower()}%"
        return (
            self.db.query(Producto)
            .filter(Producto.nombre.ilike(patron))
            .all()
        )

    def existe_codigo(self, codigo: str) -> bool:
        """Verifica si ya existe un producto con ese código."""
        return (
            self.db.query(Producto.id)
            .filter(Producto.codigo == codigo)
            .first()
            is not None
        )

    def actualizar_stock(self, producto_id: int, cantidad_vendida: int) -> Producto | None:
        """Reduce el stock de un producto tras una venta."""
        producto = self.get_by_id(producto_id)
        if producto:
            producto.stock = max(0, producto.stock - cantidad_vendida)
            self.db.commit()
            self.db.refresh(producto)
        return producto