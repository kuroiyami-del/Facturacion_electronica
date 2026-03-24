"""
schemas/schemas.py - Esquemas Pydantic para validación y serialización de la API.
Principio SRP: Cada schema tiene una única responsabilidad de validación.
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


# ── Token / Auth ──────────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── Usuario ───────────────────────────────────────────────────────────────────

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    rol: str = "FACTURADOR"


class UsuarioCreate(UsuarioBase):
    password: str
    empresa_id: int


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    empresa_id: int
    activo: bool
    ultimo_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ── Empresa ───────────────────────────────────────────────────────────────────

class EmpresaBase(BaseModel):
    nombre: str
    nit: str
    razon_social: str
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    prefijo_factura: str = "FE"
    resolucion_dian: Optional[str] = None


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaResponse(EmpresaBase):
    id: int
    activa: bool
    consecutivo_actual: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Cliente ───────────────────────────────────────────────────────────────────

class ClienteBase(BaseModel):
    tipo_documento: str = "CC"
    numero_documento: str
    tipo_persona: str = "NATURAL"
    nombre: str
    razon_social: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    razon_social: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    activo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    id: int
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Producto ──────────────────────────────────────────────────────────────────

class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    precio_unitario: Decimal
    tipo_impuesto: str = "IVA_19"
    porcentaje_iva: Decimal = Decimal("19.00")
    stock: int = 0
    unidad_medida: str = "UND"


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_unitario: Optional[Decimal] = None
    tipo_impuesto: Optional[str] = None
    stock: Optional[int] = None
    activo: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: int
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Detalle Factura ───────────────────────────────────────────────────────────

class DetalleFacturaCreate(BaseModel):
    producto_id: int
    cantidad: Decimal
    precio_unitario: Decimal
    porcentaje_descuento: Decimal = Decimal("0.00")
    porcentaje_iva: Decimal = Decimal("19.00")


class DetalleFacturaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: Decimal
    precio_unitario: Decimal
    porcentaje_descuento: Decimal
    valor_descuento: Decimal
    subtotal: Decimal
    porcentaje_iva: Decimal
    valor_iva: Decimal
    total_linea: Decimal
    producto: Optional[ProductoResponse] = None

    class Config:
        from_attributes = True


# ── Pago ──────────────────────────────────────────────────────────────────────

class PagoCreate(BaseModel):
    factura_id: int
    monto: Decimal
    medio_pago: str = "EFECTIVO"
    referencia: Optional[str] = None
    notas: Optional[str] = None


class PagoResponse(BaseModel):
    id: int
    factura_id: int
    fecha_pago: date
    monto: Decimal
    medio_pago: str
    estado: str
    referencia: Optional[str] = None

    class Config:
        from_attributes = True


# ── Factura ───────────────────────────────────────────────────────────────────

class FacturaCreate(BaseModel):
    cliente_id: int
    tipo_factura: str = "ESTANDAR"
    porcentaje_descuento: Optional[Decimal] = None
    detalles: list[DetalleFacturaCreate]
    notas: Optional[str] = None

    @field_validator("detalles")
    @classmethod
    def detalles_no_vacios(cls, v: list) -> list:
        if not v:
            raise ValueError("La factura debe tener al menos un detalle.")
        return v


class FacturaResponse(BaseModel):
    id: int
    numero_factura: str
    tipo_factura: str
    estado: str
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    subtotal: Decimal
    descuento_total: Decimal
    base_gravable: Decimal
    iva_total: Decimal
    retencion_total: Decimal
    total: Decimal
    cufe: Optional[str] = None
    validada_dian: bool
    respuesta_dian: Optional[str] = None
    notas: Optional[str] = None
    cliente: Optional[ClienteResponse] = None
    detalles: list[DetalleFacturaResponse] = []
    pagos: list[PagoResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class FacturaAnularRequest(BaseModel):
    motivo: str


class ResumenVentasResponse(BaseModel):
    total_facturas: int
    total_ventas: Decimal
    fecha_inicio: str
    fecha_fin: str