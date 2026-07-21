# Usamos una imagen oficial y ligera de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /proyecto

# Copiamos primero el archivo de dependencias (para optimizar la caché de Docker)
COPY requirements.txt .

# Instalamos los paquetes forzando a que no use caché guardada
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto al contenedor
COPY . .

# Comando por defecto al encender el contenedor (ejecuta desde la raíz hacia app/)
CMD ["python", "app/consultar_db.py"]