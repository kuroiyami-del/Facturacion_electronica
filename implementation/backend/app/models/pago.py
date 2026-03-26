"""
models/pago.py - Modelo ORM para la tabla pago.
"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, DateTime, Date, Numeric, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database.base import Base


class MedioPago(str, enum.Enum):
    EFECTIVO = "EFECTIVO"
    TRANSFERENCIA = "TRANSFERENCIA"
    TARJETA_CREDITO = "TARJETA_CREDITO"
    TARJETA_DEBITO = "TARJETA_DEBITO"
    CHEQUE = "CHEQUE"
    CREDITO = "CREDITO"


class EstadoPago(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    PAGADO = "PAGADO"
    PARCIAL = "PARCIAL"
    VENCIDO = "VENCIDO"


class Pago(Base):
    """
    Registro de un pago asociado a una factura.
    Una factura puede tener múltiples pagos (pagos parciales).
    """
    __tablename__ = "pago"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    factura_id: Mapped[int] = mapped_column(ForeignKey("factura.id"), nullable=False)
    fecha_pago: Mapped[date] = mapped_column(Date, default=date.today)
    monto: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    medio_pago: Mapped[MedioPago] = mapped_column(
        Enum(MedioPago), default=MedioPago.EFECTIVO
    )
    estado: Mapped[EstadoPago] = mapped_column(
        Enum(EstadoPago), default=EstadoPago.PENDIENTE
    )
    referencia: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaciones
    factura = relationship("Factura", back_populates="pagos")

    def __repr__(self) -> str:
        return f"<Pago(factura_id={self.factura_id}, monto={self.monto})>"