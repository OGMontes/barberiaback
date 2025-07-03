from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, delete, insert
from database import get_db
from models.barbero import Barbero
from models.barbero_servicio import barbero_servicio
from schemas.barbero import BarberoCreate, BarberoResponse
import os
import shutil
from uuid import uuid4

router = APIRouter(prefix="/barberos", tags=["Barberos"])

ASSETS_DIR = "static/barberos"

@router.post("/", response_model=BarberoResponse)
def crear_barbero(barbero: BarberoCreate, db: Session = Depends(get_db)):
    nuevo = Barbero(
        Nombre=barbero.Nombre,
        FotoUrl=barbero.FotoUrl,
        Especialidad=barbero.Especialidad,
        Activo=barbero.Activo,
        FechaIngreso=barbero.FechaIngreso or None
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # ✅ asociar servicios
    if barbero.serviciosIds:
        db.execute(insert(barbero_servicio), [
            {"BarberoId": nuevo.BarberoId, "ServicioId": sid} for sid in barbero.serviciosIds
        ])
        db.commit()

    return nuevo

@router.get("/", response_model=list[BarberoResponse])
def listar_barberos(db: Session = Depends(get_db)):
    return db.query(Barbero).options(joinedload(Barbero.servicios)).filter(Barbero.Activo == True).all()

@router.put("/{barbero_id}", response_model=BarberoResponse)
def actualizar_barbero(barbero_id: int, barbero: BarberoCreate, db: Session = Depends(get_db)):
    b = db.query(Barbero).get(barbero_id)
    if not b:
        raise HTTPException(status_code=404, detail="Barbero no encontrado")

    b.Nombre = barbero.Nombre
    b.FotoUrl = barbero.FotoUrl
    b.Especialidad = barbero.Especialidad
    b.Activo = barbero.Activo
    b.FechaIngreso = barbero.FechaIngreso
    db.commit()

    # 🔄 Actualizar relación servicios
    db.execute(delete(barbero_servicio).where(barbero_servicio.c.BarberoId == barbero_id))
    if barbero.serviciosIds:
        db.execute(insert(barbero_servicio), [
            {"BarberoId": barbero_id, "ServicioId": sid} for sid in barbero.serviciosIds
        ])
    db.commit()
    db.refresh(b)
    return b

@router.delete("/{barbero_id}")
def eliminar_barbero(barbero_id: int, db: Session = Depends(get_db)):
    barbero = db.query(Barbero).get(barbero_id)
    if not barbero:
        raise HTTPException(status_code=404, detail="No encontrado")
    barbero.Activo = False
    db.commit()
    return {"ok": True}

@router.get("/por-servicio/{servicio_id}")
def barberos_por_servicio(servicio_id: int, db: Session = Depends(get_db)):
    barberos = db.execute(
        text("""
            SELECT b.*
            FROM barberos b
            JOIN barbero_servicio bs ON b.BarberoId = bs.BarberoId
            WHERE bs.ServicioId = :servicio_id AND b.Activo = 1
        """),
        {"servicio_id": servicio_id}
    ).mappings().all()
    return barberos

@router.post("/subir-foto/{barbero_id}", response_model=BarberoResponse)
def subir_foto_barbero(barbero_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    barbero = db.query(Barbero).get(barbero_id)
    if not barbero:
        raise HTTPException(status_code=404, detail="Barbero no encontrado")

    os.makedirs(ASSETS_DIR, exist_ok=True)

    if barbero.FotoUrl and barbero.FotoUrl != "default.jpg":
        ruta_anterior = os.path.join(ASSETS_DIR, barbero.FotoUrl)
        if os.path.exists(ruta_anterior):
            os.remove(ruta_anterior)

    extension = os.path.splitext(file.filename)[1]
    nombre_archivo = f"{uuid4().hex}{extension}"
    ruta_destino = os.path.join(ASSETS_DIR, nombre_archivo)

    with open(ruta_destino, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    barbero.FotoUrl = nombre_archivo
    db.commit()
    db.refresh(barbero)

    return barbero
