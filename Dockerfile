# Usamos una imagen base de Python ligera
FROM python:3.10-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos primero los requirements para aprovechar el caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el archivo de la app
COPY emisor.py .

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando para correr la app
CMD ["uvicorn", "emisor:app", "--host", "0.0.0.0", "--port", "8000"]
