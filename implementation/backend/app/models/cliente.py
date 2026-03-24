"""
models/cliente.py - Modelo ORM para la tabla cliente.
"""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database.base import Base


class TipoDocumento(str, enum.Enum):
    CC = "CC"          # Cédula de Ciudadanía
    NIT = "NIT"        # Número de Identificación Tributaria
    CE = "CE"          # Cédula de Extranjería
    PA = "PA"          # Pasaporte
    TI = "TI"          # Tarjeta de Identidad


class TipoPersona(str, enum.Enum):
    NATURAL = "NATURAL"
    JURIDICA = "JURIDICA"


class Cliente(Base):
    """
    Representa a un cliente al que se le pueden emitir facturas electrónicas.
    """
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tipo_documento: Mapped[TipoDocumento] = mapped_column(
        Enum(TipoDocumento), default=TipoDocumento.CC
    )
    numero_documento: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True
    )
    tipo_persona: Mapped[TipoPersona] = mapped_column(
        Enum(TipoPersona), default=TipoPersona.NATURAL
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    razon_social: Mapped[str | None] = mapped_column(String(300), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    direccion: Mapped[str | None] = mapped_column(String(300), nullable=True)
    ciudad: Mapped[str | None] = mapped_column(String(100), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    facturas = relationship("Factura", back_populates="cliente")

    def __repr__(self) -> str:
        return f"<Cliente(doc={self.numero_documento}, nombre={self.nombre})>"