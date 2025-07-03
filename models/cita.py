from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from database import Base
from datetime import datetime

class Cita(Base):
    __tablename__ = "citas"

    CitaId = Column(Integer, primary_key=True, autoincrement=True)
    NombreCliente = Column(String(100), nullable=False)
    Correo = Column(String(150))
    Telefono = Column(String(20))
    FechaSolicitud = Column(DateTime, default=datetime.utcnow)
    FechaCita = Column(DateTime, nullable=False)
    ServicioId = Column(Integer, ForeignKey("servicios.ServicioId"))
    BarberoId = Column(Integer, ForeignKey("barberos.BarberoId"))
    Comentarios = Column(Text)
    Estado = Column(String(30), default="Pendiente")
