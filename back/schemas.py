from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import InvoiceStatus

# ── Auth ──────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    model_config = {"from_attributes": True}

# ── Clients ───────────────────────────────────────────
class ClientCreate(BaseModel):
    name: str
    nit: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None

class ClientUpdate(ClientCreate):
    pass

class ClientOut(ClientCreate):
    id: int
    is_active: bool
    created_at: datetime
    model_config = {"from_attributes": True}

# ── Products ──────────────────────────────────────────
class ProductCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    unit_price: float
    tax_rate: float = 19.0
    unit: str = "UND"

class ProductUpdate(ProductCreate):
    pass

class ProductOut(ProductCreate):
    id: int
    is_active: bool
    created_at: datetime
    model_config = {"from_attributes": True}

# ── Invoice Items ──────────────────────────────────────
class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    tax_rate: float = 19.0

class InvoiceItemOut(BaseModel):
    id: int
    product_id: int
    quantity: float
    unit_price: float
    tax_rate: float
    subtotal: float
    tax_amount: float
    total: float
    product: ProductOut
    model_config = {"from_attributes": True}

# ── Invoices ──────────────────────────────────────────
class InvoiceCreate(BaseModel):
    client_id: int
    notes: Optional[str] = None
    items: List[InvoiceItemCreate]

class InvoiceOut(BaseModel):
    id: int
    number: str
    client_id: int
    status: InvoiceStatus
    subtotal: float
    tax_amount: float
    total: float
    notes: Optional[str]
    cufe: Optional[str]
    issued_at: datetime
    client: ClientOut
    items: List[InvoiceItemOut]
    model_config = {"from_attributes": True}

class InvoiceListOut(BaseModel):
    id: int
    number: str
    status: InvoiceStatus
    total: float
    issued_at: datetime
    client: ClientOut
    model_config = {"from_attributes": True}

# ── Dashboard ─────────────────────────────────────────
class DashboardStats(BaseModel):
    total_invoices: int
    total_revenue: float
    invoices_sent: int
    invoices_accepted: int
    invoices_this_month: int
    revenue_this_month: float
    top_clients: List[dict]
