from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.cita import Cita
from schemas.cita import CitaCreate, CitaResponse, CitaUpdate
from pytz import timezone
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()
router = APIRouter(prefix="/citas", tags=["Citas"])

@router.post("/", response_model=CitaResponse)
def crear_cita(cita_data: CitaCreate, db: Session = Depends(get_db)):
    tz = timezone('America/Mexico_City')
    fecha_local = cita_data.FechaCita.astimezone(tz)

    cita = Cita(
        NombreCliente=cita_data.NombreCliente,
        Correo=cita_data.Correo,
        Telefono=cita_data.Telefono,
        FechaCita=cita_data.FechaCita,
        ServicioId=cita_data.ServicioId,
        BarberoId=cita_data.BarberoId,
        Comentarios=cita_data.Comentarios,
        Estado="Pendiente"
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)

    fecha_str = fecha_local.strftime("%d/%m/%Y %H:%M")
    telefono = cita.Telefono
    if not telefono.startswith("+52"):
        telefono = f"+52{telefono}"

    mensaje = f"Hola {cita.NombreCliente}, tu cita fue agendada para el {fecha_str}. ¡Gracias por elegirnos!"
    enviar_mensaje_twilio(telefono, mensaje)

    return cita

@router.get("/", response_model=list[CitaResponse])
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Cita).order_by(Cita.FechaCita).all()

@router.put("/{cita_id}", response_model=CitaResponse)
def actualizar_cita(cita_id: int, datos: CitaUpdate, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.CitaId == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(cita, key, value)

    db.commit()
    db.refresh(cita)
    return cita

@router.delete("/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = db.query(Cita).filter(Cita.CitaId == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    db.delete(cita)
    db.commit()
    return {"mensaje": "Cita eliminada correctamente"}

def enviar_mensaje_twilio(to: str, mensaje: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        print("❌ Faltan variables de entorno")
        return

    url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'
    data = {
        'To': to,
        'From': from_number,
        'Body': mensaje
    }

    response = requests.post(url, data=data, auth=HTTPBasicAuth(account_sid, auth_token))

    if response.status_code == 201:
        print("✅ Mensaje enviado")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
