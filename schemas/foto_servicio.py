# schemas/foto_servicio.py
from pydantic import BaseModel

class FotoServicioBase(BaseModel):
    ServicioId: int
    Url: str

class FotoServicioCreate(FotoServicioBase):
    pass

class FotoServicioResponse(FotoServicioBase):
    FotoId: int

    class Config:
        orm_mode = True
