"""
routers/clientes.py - CRUD de clientes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.repositories.cliente_repository import ClienteRepository
from app.routers.dependencies import get_usuario_actual
from app.schemas.schemas import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(
    skip: int = 0,
    limit: int = 100,
    buscar: str | None = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Lista todos los clientes activos. Soporta búsqueda por nombre."""
    repo = ClienteRepository(db)
    if buscar:
        return repo.buscar_por_nombre(buscar)
    return repo.get_activos(skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Retorna los datos de un cliente específico por ID."""
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    return cliente


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    payload: ClienteCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Registra un nuevo cliente."""
    repo = ClienteRepository(db)
    if repo.existe_documento(payload.numero_documento):
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un cliente con el documento {payload.numero_documento}.",
        )
    cliente = Cliente(**payload.model_dump())
    return repo.create(cliente)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(
    cliente_id: int,
    payload: ClienteUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Actualiza los datos de un cliente existente."""
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")

    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)
    return repo.update(cliente)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Desactiva un cliente (soft delete)."""
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    cliente.activo = False
    repo.update(cliente)