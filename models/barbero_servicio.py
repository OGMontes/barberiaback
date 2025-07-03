from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

barbero_servicio = Table(
    'barbero_servicio',
    Base.metadata,
    Column('BarberoId', Integer, ForeignKey('barberos.BarberoId'), primary_key=True),
    Column('ServicioId', Integer, ForeignKey('servicios.ServicioId'), primary_key=True)
)
