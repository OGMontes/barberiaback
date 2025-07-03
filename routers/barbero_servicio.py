from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.barbero_servicio import barbero_servicio
from sqlalchemy import insert, select

router = APIRouter(prefix="/barbero-servicio", tags=["BarberoServicio"])

@router.post("/")
def asignar_servicio(barbero_id: int, servicio_id: int, db: Session = Depends(get_db)):
    stmt = insert(barbero_servicio).values(BarberoId=barbero_id, ServicioId=servicio_id)
    db.execute(stmt)
    db.commit()
    return {"mensaje": "Servicio asignado al barbero correctamente"}

@router.get("/")
def listar_relaciones(db: Session = Depends(get_db)):
    result = db.execute(select(barbero_servicio)).fetchall()
    return [dict(r._mapping) for r in result]
