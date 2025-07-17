from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CitaCreate(BaseModel):
    NombreCliente: str
    Correo: str
    Telefono: str
    FechaCita: datetime
    ServicioId: int
    BarberoId: int
    Comentarios: Optional[str] = None

class CitaUpdate(BaseModel):
    NombreCliente: Optional[str]
    Correo: Optional[str]
    Telefono: Optional[str]
    FechaCita: Optional[datetime]
    ServicioId: Optional[int]
    BarberoId: Optional[int]
    Comentarios: Optional[str]
    Estado: Optional[str]

class CitaResponse(CitaCreate):
    CitaId: int
    Estado: str

    class Config:
        orm_mode = True
