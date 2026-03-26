"""
database/base.py - Base declarativa de SQLAlchemy.
Todos los modelos heredan de esta clase para registrarse en el metadata.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM de FactuPlus."""
    pass