"""
models/empresa.py - Modelo ORM para la tabla empresa.
Principio SRP: Este modelo solo describe la estructura de datos de Empresa.
"""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Empresa(Base):
    """
    Representa la empresa emisora de facturas electrónicas.
    Una instancia única configura el sistema completo.
    """
    __tablename__ = "empresa"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    nit: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    razon_social: Mapped[str] = mapped_column(String(300), nullable=False)
    direccion: Mapped[str] = mapped_column(String(300), nullable=True)
    ciudad: Mapped[str] = mapped_column(String(100), nullable=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=True)
    regimen: Mapped[str] = mapped_column(String(50), default="RESPONSABLE_IVA")
    activa: Mapped[bool] = mapped_column(Boolean, default=True)
    prefijo_factura: Mapped[str] = mapped_column(String(10), default="FE")
    consecutivo_actual: Mapped[int] = mapped_column(default=1)
    resolucion_dian: Mapped[str | None] = mapped_column(String(100), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    usuarios = relationship("Usuario", back_populates="empresa")
    facturas = relationship("Factura", back_populates="empresa")

    def __repr__(self) -> str:
        return f"<Empresa(nit={self.nit}, nombre={self.nombre})>"