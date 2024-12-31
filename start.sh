#!/bin/bash

# Actualiza los paquetes e instala las dependencias necesarias para dlib
apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev

# Instalar pip, si no está actualizado
pip install --upgrade pip

# Instalar las dependencias de Python desde requirements.txt
pip install -r requirements.txt

# Ejecutar la aplicación
python3 app.py
