from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.servicio import Servicio as ServicioModel
from schemas.servicio import ServicioCreate, ServicioResponse

router = APIRouter(prefix="/servicios", tags=["servicios"])

@router.post("/", response_model=ServicioResponse)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    nuevo = ServicioModel(**servicio.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[ServicioResponse])
def listar_servicios(db: Session = Depends(get_db)):
    return db.query(ServicioModel).filter(ServicioModel.Activo == True).all()

@router.put("/{servicio_id}", response_model=ServicioResponse)
def actualizar_servicio(servicio_id: int, datos: ServicioCreate, db: Session = Depends(get_db)):
    servicio = db.query(ServicioModel).get(servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    servicio.Nombre = datos.Nombre
    servicio.duracion_minutos = datos.duracion_minutos
    servicio.Precio = datos.Precio
    servicio.Descripcion = datos.Descripcion

    db.commit()
    db.refresh(servicio)
    return servicio


@router.delete("/{servicio_id}")
def eliminar_servicio(servicio_id: int, db: Session = Depends(get_db)):
    servicio = db.query(ServicioModel).get(servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    servicio.Activo = False
    db.commit()
    return {"ok": True}

    
