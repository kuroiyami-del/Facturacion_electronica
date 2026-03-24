"""
repositories/factura_repository.py - Acceso a datos para Factura y DetalleFactura.
"""
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload

from app.models.factura import Factura, DetalleFactura, EstadoFactura
from app.repositories.base_repository import BaseRepository


class FacturaRepository(BaseRepository[Factura]):
    """
    Repositorio especializado para la entidad Factura.
    Incluye consultas optimizadas con eager loading para evitar el problema N+1.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(Factura, db)

    def get_by_numero(self, numero_factura: str) -> Factura | None:
        """Busca una factura por su número único."""
        return (
            self.db.query(Factura)
            .options(
                joinedload(Factura.cliente),
                joinedload(Factura.detalles).joinedload(DetalleFactura.producto),
            )
            .filter(Factura.numero_factura == numero_factura)
            .first()
        )

    def get_con_detalles(self, factura_id: int) -> Factura | None:
        """Carga una factura con todos sus detalles en una sola query (evita N+1)."""
        return (
            self.db.query(Factura)
            .options(
                joinedload(Factura.cliente),
                joinedload(Factura.empresa),
                joinedload(Factura.usuario),
                joinedload(Factura.detalles).joinedload(DetalleFactura.producto),
                joinedload(Factura.pagos),
            )
            .filter(Factura.id == factura_id)
            .first()
        )

    def get_por_cliente(self, cliente_id: int) -> list[Factura]:
        """Retorna el historial de facturas de un cliente específico."""
        return (
            self.db.query(Factura)
            .filter(Factura.cliente_id == cliente_id)
            .order_by(Factura.fecha_emision.desc())
            .all()
        )

    def get_por_estado(self, estado: EstadoFactura) -> list[Factura]:
        """Filtra facturas por estado (EMITIDA, VALIDADA_DIAN, etc.)."""
        return (
            self.db.query(Factura)
            .filter(Factura.estado == estado)
            .order_by(Factura.created_at.desc())
            .all()
        )

    def get_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date) -> list[Factura]:
        """Obtiene facturas emitidas en un rango de fechas."""
        return (
            self.db.query(Factura)
            .filter(
                Factura.fecha_emision >= fecha_inicio,
                Factura.fecha_emision <= fecha_fin,
            )
            .order_by(Factura.fecha_emision.desc())
            .all()
        )

    def get_ultimo_consecutivo(self, empresa_id: int, prefijo: str) -> int:
        """Obtiene el último número de consecutivo para generar el siguiente."""
        ultima_factura = (
            self.db.query(Factura)
            .filter(
                Factura.empresa_id == empresa_id,
                Factura.numero_factura.like(f"{prefijo}%"),
            )
            .order_by(Factura.id.desc())
            .first()
        )
        if ultima_factura is None:
            return 0
        sufijo = ultima_factura.numero_factura.replace(prefijo, "")
        return int(sufijo) if sufijo.isdigit() else 0

    def total_ventas_periodo(self, fecha_inicio: date, fecha_fin: date) -> Decimal:
        """Calcula el total de ventas en un período dado."""
        from sqlalchemy import func
        result = (
            self.db.query(func.sum(Factura.total))
            .filter(
                Factura.fecha_emision >= fecha_inicio,
                Factura.fecha_emision <= fecha_fin,
                Factura.estado != EstadoFactura.ANULADA,
            )
            .scalar()
        )
        return result or Decimal("0.00")

    def actualizar_estado(self, factura_id: int, nuevo_estado: EstadoFactura) -> Factura | None:
        """Actualiza el estado de una factura."""
        factura = self.get_by_id(factura_id)
        if factura:
            factura.estado = nuevo_estado
            self.db.commit()
            self.db.refresh(factura)
        return factura