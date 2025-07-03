from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.cita import Cita
from schemas.cita import CitaCreate, CitaResponse

router = APIRouter(prefix="/citas", tags=["Citas"])

@router.post("/", response_model=CitaResponse)
def crear_cita(cita_data: CitaCreate, db: Session = Depends(get_db)):
    cita = Cita(
        NombreCliente=cita_data.NombreCliente,
        Correo=cita_data.Correo,
        Telefono=cita_data.Telefono,
        FechaCita=cita_data.FechaCita,
        ServicioId=cita_data.ServicioId,
        BarberoId=cita_data.BarberoId,
        Comentarios=cita_data.Comentarios,
        Estado="Pendiente"
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

@router.get("/", response_model=list[CitaResponse])
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).order_by(Cita.FechaCita).all()


from schemas.cita import CitaUpdate  # asegúrate de importar esto

@router.put("/{cita_id}", response_model=CitaResponse)
def actualizar_cita(
    cita_id: int,
    datos: CitaUpdate,
    db: Session = Depends(get_db)
):
    cita = db.query(Cita).filter(Cita.CitaId == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(cita, key, value)

    db.commit()
    db.refresh(cita)
    return cita

@router.delete("/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.CitaId == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    db.delete(cita)
    db.commit()
    return {"mensaje": "Cita eliminada correctamente"}

