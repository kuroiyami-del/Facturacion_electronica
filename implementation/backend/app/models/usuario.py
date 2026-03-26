"""
models/usuario.py - Modelo ORM para la tabla usuario.
"""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database.base import Base


class RolUsuario(str, enum.Enum):
    ADMIN = "ADMIN"
    FACTURADOR = "FACTURADOR"
    AUDITOR = "AUDITOR"


class Usuario(Base):
    """
    Representa un usuario del sistema con credenciales y rol asignado.
    """
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresa.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    apellido: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(
        Enum(RolUsuario), default=RolUsuario.FACTURADOR
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    ultimo_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    empresa = relationship("Empresa", back_populates="usuarios")
    facturas = relationship("Factura", back_populates="usuario")

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __repr__(self) -> str:
        return f"<Usuario(email={self.email}, rol={self.rol})>"