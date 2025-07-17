# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import get_db, Base, engine
from routers import barberos, servicios, citas, barbero_servicio, fotos_servicio

# Asegurarse de que las tablas están creadas
Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api-barber")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:5096",
        "https://portafolio.tecnocoremexico.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar estáticos
app.mount(
    "/barberos-img",
    StaticFiles(directory="static/barberos"),
    name="barberos-img",
)
app.mount(
    "/cortes-img",
    StaticFiles(directory="static/cortes"),
    name="cortes-img",
)
app.mount(
    "/fotos-servicio",
    StaticFiles(directory="static/fotos-servicio"),
    name="fotos-servicio",
)

# Routers
app.include_router(barberos.router)
app.include_router(servicios.router)
app.include_router(citas.router)
app.include_router(barbero_servicio.router)
app.include_router(
    fotos_servicio.router,
    prefix="/api-fotos-servicio",
)
