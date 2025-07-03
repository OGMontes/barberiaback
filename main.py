from fastapi import FastAPI
from routers import barberos, servicios, citas, barbero_servicio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(root_path="/api-barber")




# 💻 Luego aplicas el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # para desarrollo local
        "http://localhost:5096",
        "http://0.0.0.0:5096",
        "https://portafolio.tecnocoremexico.com",        # producción frontend
        "https://portafolio.tecnocoremexico.com:5096",   # producción backend si lo llamas directamente
        "http://74.208.14.192:8443"  # IP con puerto por si pruebas directo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# 📦 Incluye tus routers
app.include_router(barberos.router)
app.include_router(servicios.router)
app.include_router(citas.router)
app.include_router(barbero_servicio.router)
app.mount("/barberos-img", StaticFiles(directory="static/barberos"), name="barberos-img")
