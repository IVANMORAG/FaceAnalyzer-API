FROM python:3.12-buster

# Instalar dependencias del sistema necesarias para dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear el directorio de trabajo y copiar el código
WORKDIR /app
COPY . .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto y correr la app
EXPOSE 5000
CMD ["python", "app.py"]
