FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    libssl-dev \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Configuración de trabajo
WORKDIR /app

# Copiar los archivos del backend
COPY . /app

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]