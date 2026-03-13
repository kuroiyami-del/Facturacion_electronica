from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class InvoiceStatus(str, enum.Enum):
    DRAFT = "BORRADOR"
    SENT = "ENVIADA"
    ACCEPTED = "ACEPTADA"
    REJECTED = "RECHAZADA"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    nit = Column(String(20), unique=True, index=True, nullable=False)  # NIT colombiano
    email = Column(String(150))
    phone = Column(String(20))
    address = Column(String(300))
    city = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    invoices = relationship("Invoice", back_populates="client")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=19.0)  # IVA Colombia 19%
    unit = Column(String(50), default="UND")  # Unidad de medida DIAN
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    invoice_items = relationship("InvoiceItem", back_populates="product")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False)  # Ej: FE-0001
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    subtotal = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    notes = Column(Text)
    cufe = Column(String(255))          # Código único DIAN
    dian_response = Column(Text)        # Respuesta XML de la DIAN
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    client = relationship("Client", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=19.0)
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="invoice_items")
