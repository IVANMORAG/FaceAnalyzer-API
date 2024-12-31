# Usa una imagen base de Python (elige una versión compatible con tu aplicación)
FROM python:3.12-slim

# Actualiza pip
RUN pip install --upgrade pip

# Instala las dependencias del sistema necesarias para compilar dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . .

# Instala las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que Flask corre
EXPOSE 5000

# Define el comando de inicio para la aplicación
CMD ["python", "app.py"]
