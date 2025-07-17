# models/foto_servicio.py
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class FotoServicio(Base):
    __tablename__ = "fotos_servicio"

    FotoId      = Column(Integer, primary_key=True, index=True)
    ServicioId  = Column(Integer, ForeignKey("servicios.ServicioId"), nullable=False)
    Url         = Column(String(255), nullable=False)
