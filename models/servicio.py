from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL
from sqlalchemy.orm import relationship
from database import Base
from models.barbero_servicio import barbero_servicio

class Servicio(Base):
    __tablename__ = 'servicios'

    ServicioId = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(Text)
    duracion_minutos = Column(Integer)
    Precio = Column(DECIMAL(10, 2), nullable=False)
    Activo = Column(Boolean, default=True)

    barberos = relationship(
        "Barbero",
        secondary=barbero_servicio,
        back_populates="servicios"
    )
