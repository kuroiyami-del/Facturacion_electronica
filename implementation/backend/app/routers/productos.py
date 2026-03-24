"""
routers/productos.py - CRUD de productos/servicios.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.repositories.producto_repository import ProductoRepository
from app.routers.dependencies import get_usuario_actual
from app.schemas.schemas import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=list[ProductoResponse])
def listar_productos(
    skip: int = 0,
    limit: int = 100,
    buscar: str | None = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Lista todos los productos activos del catálogo."""
    repo = ProductoRepository(db)
    if buscar:
        return repo.buscar_por_nombre(buscar)
    return repo.get_activos(skip=skip, limit=limit)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Retorna los datos de un producto por ID."""
    repo = ProductoRepository(db)
    producto = repo.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    payload: ProductoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Agrega un nuevo producto al catálogo."""
    repo = ProductoRepository(db)
    if repo.existe_codigo(payload.codigo):
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un producto con el código {payload.codigo}.",
        )
    producto = Producto(**payload.model_dump())
    return repo.create(producto)


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    payload: ProductoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Actualiza los datos de un producto existente."""
    repo = ProductoRepository(db)
    producto = repo.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)
    return repo.update(producto)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_actual),
):
    """Desactiva un producto del catálogo (soft delete)."""
    repo = ProductoRepository(db)
    producto = repo.get_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    producto.activo = False
    repo.update(producto)