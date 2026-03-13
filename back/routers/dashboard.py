from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from database import get_db
from models import Invoice, Client, InvoiceStatus
from schemas import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    now = datetime.utcnow()

    total_invoices = db.query(Invoice).count()
    total_revenue = db.query(func.sum(Invoice.total)).filter(
        Invoice.status == InvoiceStatus.ACCEPTED
    ).scalar() or 0.0

    invoices_sent = db.query(Invoice).filter(Invoice.status == InvoiceStatus.SENT).count()
    invoices_accepted = db.query(Invoice).filter(Invoice.status == InvoiceStatus.ACCEPTED).count()

    invoices_this_month = db.query(Invoice).filter(
        extract("month", Invoice.issued_at) == now.month,
        extract("year", Invoice.issued_at) == now.year,
    ).count()

    revenue_this_month = db.query(func.sum(Invoice.total)).filter(
        Invoice.status == InvoiceStatus.ACCEPTED,
        extract("month", Invoice.issued_at) == now.month,
        extract("year", Invoice.issued_at) == now.year,
    ).scalar() or 0.0

    # Top 5 clientes por valor facturado
    top_clients_query = (
        db.query(Client.name, func.sum(Invoice.total).label("total"))
        .join(Invoice, Invoice.client_id == Client.id)
        .group_by(Client.id, Client.name)
        .order_by(func.sum(Invoice.total).desc())
        .limit(5)
        .all()
    )
    top_clients = [{"name": name, "total": float(total)} for name, total in top_clients_query]

    return DashboardStats(
        total_invoices=total_invoices,
        total_revenue=total_revenue,
        invoices_sent=invoices_sent,
        invoices_accepted=invoices_accepted,
        invoices_this_month=invoices_this_month,
        revenue_this_month=revenue_this_month,
        top_clients=top_clients,
    )
