"""
models/factura.py - Modelos ORM para factura y detalle_factura.
"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, DateTime, Date, Numeric, Integer, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database.base import Base


class EstadoFactura(str, enum.Enum):
    BORRADOR = "BORRADOR"
    EMITIDA = "EMITIDA"
    VALIDADA_DIAN = "VALIDADA_DIAN"
    RECHAZADA = "RECHAZADA"
    ANULADA = "ANULADA"


class TipoFactura(str, enum.Enum):
    ESTANDAR = "ESTANDAR"
    CON_DESCUENTO = "CON_DESCUENTO"
    CON_RETENCION = "CON_RETENCION"
    EXPORTACION = "EXPORTACION"


class Factura(Base):
    """
    Cabecera de la factura electrónica. Contiene información del emisor,
    receptor, totales y estado de validación DIAN.
    """
    __tablename__ = "factura"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresa.id"), nullable=False)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)

    # Numeración
    numero_factura: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    tipo_factura: Mapped[TipoFactura] = mapped_column(
        Enum(TipoFactura), default=TipoFactura.ESTANDAR
    )
    estado: Mapped[EstadoFactura] = mapped_column(
        Enum(EstadoFactura), default=EstadoFactura.BORRADOR
    )

    # Fechas
    fecha_emision: Mapped[date] = mapped_column(Date, default=date.today)
    fecha_vencimiento: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Valores económicos
    subtotal: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))
    descuento_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))
    base_gravable: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))
    iva_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))
    retencion_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))
    total: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))

    # DIAN
    cufe: Mapped[str | None] = mapped_column(String(200), nullable=True)   # Código Único de Factura Electrónica
    qr_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    validada_dian: Mapped[bool] = mapped_column(Boolean, default=False)
    respuesta_dian: Mapped[str | None] = mapped_column(Text, nullable=True)

    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    empresa = relationship("Empresa", back_populates="facturas")
    cliente = relationship("Cliente", back_populates="facturas")
    usuario = relationship("Usuario", back_populates="facturas")
    detalles = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="factura", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Factura(numero={self.numero_factura}, total={self.total})>"


class DetalleFactura(Base):
    """
    Línea de detalle de una factura: producto, cantidad, precios e impuestos.
    """
    __tablename__ = "detalle_factura"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    factura_id: Mapped[int] = mapped_column(ForeignKey("factura.id"), nullable=False)
    producto_id: Mapped[int] = mapped_column(ForeignKey("producto.id"), nullable=False)

    cantidad: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    porcentaje_descuento: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"))
    valor_descuento: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    porcentaje_iva: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("19.00"))
    valor_iva: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))
    total_linea: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    # Relaciones
    factura = relationship("Factura", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")

    def __repr__(self) -> str:
        return f"<DetalleFactura(factura_id={self.factura_id}, producto_id={self.producto_id})>"