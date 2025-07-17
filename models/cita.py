from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base

class Cita(Base):
    __tablename__ = "citas"

    CitaId = Column(Integer, primary_key=True, index=True)
    NombreCliente = Column(String)
    Correo = Column(String)
    Telefono = Column(String)
    FechaCita = Column(DateTime)
    ServicioId = Column(Integer)
    BarberoId = Column(Integer)
    Comentarios = Column(String)
    Estado = Column(String)
