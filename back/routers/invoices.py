from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Invoice, InvoiceItem, InvoiceStatus
from schemas import InvoiceCreate, InvoiceOut, InvoiceListOut

router = APIRouter(prefix="/invoices", tags=["Facturas"])

def generate_invoice_number(db: Session) -> str:
    count = db.query(Invoice).count() + 1
    return f"FE-{count:04d}"

def calculate_item_totals(item_data):
    subtotal = item_data.quantity * item_data.unit_price
    tax_amount = subtotal * (item_data.tax_rate / 100)
    total = subtotal + tax_amount
    return subtotal, tax_amount, total

@router.get("/", response_model=List[InvoiceListOut])
def list_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Invoice).order_by(Invoice.issued_at.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=InvoiceOut, status_code=201)
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    if not data.items:
        raise HTTPException(status_code=400, detail="La factura debe tener al menos un ítem")

    invoice = Invoice(
        number=generate_invoice_number(db),
        client_id=data.client_id,
        notes=data.notes,
    )
    db.add(invoice)
    db.flush()  # Obtener el ID sin hacer commit

    invoice_subtotal = 0.0
    invoice_tax = 0.0

    for item_data in data.items:
        subtotal, tax_amount, total = calculate_item_totals(item_data)
        item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            tax_rate=item_data.tax_rate,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total=total,
        )
        db.add(item)
        invoice_subtotal += subtotal
        invoice_tax += tax_amount

    invoice.subtotal = invoice_subtotal
    invoice.tax_amount = invoice_tax
    invoice.total = invoice_subtotal + invoice_tax

    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return invoice

@router.patch("/{invoice_id}/send", response_model=InvoiceOut)
def send_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Marcar factura como enviada (preparado para integración DIAN)"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    if invoice.status != InvoiceStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Solo se pueden enviar facturas en borrador")
    invoice.status = InvoiceStatus.SENT
    db.commit()
    db.refresh(invoice)
    return invoice

@router.delete("/{invoice_id}", status_code=204)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    if invoice.status != InvoiceStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Solo se pueden eliminar facturas en borrador")
    db.delete(invoice)
    db.commit()
