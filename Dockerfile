# Imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 80

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
