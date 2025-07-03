from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from models.barbero_servicio import barbero_servicio

class Barbero(Base):
    __tablename__ = "barberos"

    BarberoId = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    FotoUrl = Column(String(255), nullable=True)
    Especialidad = Column(String(100), nullable=True)
    Activo = Column(Boolean, default=True)
    FechaIngreso = Column(DateTime, default=datetime.utcnow)

    servicios = relationship(
        "Servicio",
        secondary=barbero_servicio,
        back_populates="barberos"
    )
