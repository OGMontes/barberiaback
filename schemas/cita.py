from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CitaCreate(BaseModel):
    NombreCliente: str
    Correo: Optional[str]
    Telefono: str
    FechaCita: datetime
    ServicioId: int
    BarberoId: int
    Comentarios: Optional[str] = ""
    
class CitaResponse(CitaCreate):
    CitaId: int
    Estado: str
    FechaSolicitud: datetime

    class Config:
        from_attributes = True  # reemplaza orm_mode

class CitaUpdate(BaseModel):
    Estado: Optional[str] = None
    FechaCita: Optional[datetime] = None
    BarberoId: Optional[int] = None
    Comentarios: Optional[str] = None