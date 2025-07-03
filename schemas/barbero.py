from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from schemas.servicio import ServicioResponse

class BarberoBase(BaseModel):
    Nombre: str
    FotoUrl: Optional[str] = None
    Especialidad: Optional[str] = None
    Activo: Optional[bool] = True
    FechaIngreso: Optional[datetime] = None

class BarberoCreate(BarberoBase):
    serviciosIds: List[int] = []  # ✅ lista de habilidades (servicios)

class BarberoResponse(BarberoBase):
    BarberoId: int
    servicios: List[ServicioResponse] = []

    class Config:
        from_attributes = True
