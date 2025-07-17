# routers/fotos_servicio.py
import os
import shutil
from uuid import uuid4
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session

from database   import get_db
from models.foto_servicio import FotoServicio
from schemas.foto_servicio import FotoServicioCreate, FotoServicioResponse

router = APIRouter(
    prefix="/api-fotos-servicio",
    tags=["fotos-servicio"]
)

# Directorio donde se guardan los archivos subidos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "static", "fotos-servicio")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post(
    "/{servicio_id}",
    response_model=List[FotoServicioResponse],
    summary="Subir una o varias fotos para un servicio"
)
async def subir_fotos(
    servicio_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    resultados = []
    for file in files:
        ext = os.path.splitext(file.filename)[1]
        nombre = f"{servicio_id}_{uuid4().hex}{ext}"
        destino = os.path.join(UPLOAD_DIR, nombre)
        with open(destino, "wb") as f:
            shutil.copyfileobj(file.file, f)
        foto = FotoServicio(ServicioId=servicio_id, Url=nombre)
        db.add(foto)
        db.commit()
        db.refresh(foto)
        resultados.append(foto)
    return resultados

@router.get(
    "/{servicio_id}",
    response_model=List[FotoServicioResponse],
    summary="Listar todas las fotos de un servicio"
)
def listar_fotos(servicio_id: int, db: Session = Depends(get_db)):
    return (
        db.query(FotoServicio)
          .filter(FotoServicio.ServicioId == servicio_id)
          .order_by(FotoServicio.FotoId)
          .all()
    )

@router.delete(
    "/{foto_id}",
    summary="Eliminar una foto y su registro de la BD"
)
def eliminar_foto(foto_id: int, db: Session = Depends(get_db)):
    foto = db.query(FotoServicio).get(foto_id)
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    # Borrar archivo
    path = os.path.join(UPLOAD_DIR, foto.Url)
    if os.path.exists(path):
        os.remove(path)
    # Borrar de la BD
    db.delete(foto)
    db.commit()
    return {"ok": True}
