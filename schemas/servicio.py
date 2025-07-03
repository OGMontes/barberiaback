from pydantic import BaseModel
from typing import Optional

class ServicioBase(BaseModel):
    Nombre: str
    Descripcion: Optional[str] = None
    duracion_minutos: Optional[int]
    Precio: float
    Activo: Optional[bool] = True

class ServicioCreate(ServicioBase):
    pass

class ServicioResponse(ServicioBase):
    ServicioId: int

    class Config:
        from_attributes = True
