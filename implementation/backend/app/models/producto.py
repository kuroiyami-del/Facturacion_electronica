"""
models/producto.py - Modelo ORM para la tabla producto.
"""
from datetime import datetime
from sqlalchemy import String, Numeric, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database.base import Base


class TipoImpuesto(str, enum.Enum):
    """Tipos de impuesto según normativa colombiana."""
    IVA_0 = "0"          # Exento o 0%
    IVA_5 = "5"          # 5% (algunos productos específicos)
    IVA_19 = "19"        # Tarifa general 19%
    EXENTO = "EXENTO"    # Exento de IVA


class Producto(Base):
    """
    Representa un producto o servicio del catálogo.
    """
    __tablename__ = "producto"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(500), nullable=True)
    precio_unitario: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    tipo_impuesto: Mapped[TipoImpuesto] = mapped_column(
        Enum(TipoImpuesto), nullable=False, default=TipoImpuesto.IVA_19
    )
    porcentaje_iva: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    stock: Mapped[int] = mapped_column(default=0)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    detalles = relationship("DetalleFactura", back_populates="producto")

    def __repr__(self) -> str:
        return f"<Producto(codigo={self.codigo}, nombre={self.nombre}, precio={self.precio_unitario})>"