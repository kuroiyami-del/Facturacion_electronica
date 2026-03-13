from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Client
from schemas import ClientCreate, ClientUpdate, ClientOut

router = APIRouter(prefix="/clients", tags=["Clientes"])

@router.get("/", response_model=List[ClientOut])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Client).filter(Client.is_active == True).offset(skip).limit(limit).all()

@router.post("/", response_model=ClientOut, status_code=201)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    if db.query(Client).filter(Client.nit == data.nit).first():
        raise HTTPException(status_code=400, detail="El NIT ya está registrado")
    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, data: ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    client.is_active = False  # Soft delete
    db.commit()
