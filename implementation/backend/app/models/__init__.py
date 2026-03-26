"""
models/__init__.py - Exporta todos los modelos para que SQLAlchemy los registre.
Es fundamental importarlos antes de llamar a Base.metadata.create_all().
"""
from app.models.empresa import Empresa
from app.models.usuario import Usuario, RolUsuario
from app.models.cliente import Cliente, TipoDocumento, TipoPersona
from app.models.producto import Producto, TipoImpuesto
from app.models.factura import Factura, DetalleFactura, EstadoFactura, TipoFactura
from app.models.pago import Pago, MedioPago, EstadoPago

__all__ = [
    "Empresa",
    "Usuario",
    "RolUsuario",
    "Cliente",
    "TipoDocumento",
    "TipoPersona",
    "Producto",
    "TipoImpuesto",
    "Factura",
    "DetalleFactura",
    "EstadoFactura",
    "TipoFactura",
    "Pago",
    "MedioPago",
    "EstadoPago",
]