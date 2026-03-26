from app.repositories.base_repository import BaseRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.factura_repository import FacturaRepository

__all__ = [
    "BaseRepository",
    "UsuarioRepository",
    "ClienteRepository",
    "ProductoRepository",
    "FacturaRepository",
]