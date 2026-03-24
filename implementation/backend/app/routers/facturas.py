"""
routers/facturas.py - Endpoints del módulo de facturación electrónica.
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.repositories.factura_repository import FacturaRepository
from app.routers.dependencies import get_usuario_actual
from app.schemas.schemas import (
    FacturaCreate,
    FacturaResponse,
    FacturaAnularRequest,
    ResumenVentasResponse,
)
from app.services.factura_service import FacturaService

router = APIRouter(prefix="/facturas", tags=["Facturas"])


def _obtener_empresa(db: Session, usuario: Usuario) -> Empresa:
    """Obtiene la empresa del usuario autenticado."""
    empresa = db.get(Empresa, usuario.empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa del usuario no encontrada.")
    return empresa


@router.get("/", response_model=list[FacturaResponse])
def listar_facturas(
    fecha_inicio: date | None = Query(None),
    fecha_fin: date | None = Query(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    """Lista facturas con filtro opcional por rango de fechas."""
    service = FacturaService(db)
    return service.obtener_historial(fecha_inicio, fecha_fin)


@router.get("/resumen", response_model=ResumenVentasResponse)
def resumen_ventas(
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Retorna el resumen de ventas para el período solicitado."""
    service = FacturaService(db)
    return service.resumen_ventas(fecha_inicio, fecha_fin)


@router.get("/{factura_id}", response_model=FacturaResponse)
def obtener_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Retorna una factura con todos sus detalles y pagos."""
    repo = FacturaRepository(db)
    factura = repo.get_con_detalles(factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada.")
    return factura


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
def crear_factura(
    payload: FacturaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_actual),
):
    """
    Crea una nueva factura en estado BORRADOR.
    Soporta los tipos: ESTANDAR, CON_DESCUENTO, CON_RETENCION, EXPORTACION.
    """
    empresa = _obtener_empresa(db, usuario)
    service = FacturaService(db)

    detalles_data = [d.model_dump() for d in payload.detalles]
    try:
        factura = service.crear_factura(
            empresa=empresa,
            cliente_id=payload.cliente_id,
            usuario_id=usuario.id,
            detalles_data=detalles_data,
            tipo_factura=payload.tipo_factura,
            porcentaje_descuento=payload.porcentaje_descuento,
            notas=payload.notas,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return factura


@router.post("/{factura_id}/emitir", response_model=FacturaResponse)
def emitir_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """
    Emite una factura (BORRADOR → EMITIDA → VALIDADA_DIAN).
    Dispara el flujo completo: notificaciones + validación DIAN.
    """
    service = FacturaService(db)
    try:
        return service.emitir_factura(factura_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/{factura_id}/anular", response_model=FacturaResponse)
def anular_factura(
    factura_id: int,
    payload: FacturaAnularRequest,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Anula una factura existente con un motivo obligatorio."""
    service = FacturaService(db)
    try:
        return service.anular_factura(factura_id, payload.motivo)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))