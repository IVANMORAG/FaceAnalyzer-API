# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos de la aplicación al contenedor
COPY . /app/

# Expone el puerto en el que Flask escucha (por defecto 5000)
EXPOSE 5000

# Usa el comando de ejecución adecuado para la aplicación Flask
ENTRYPOINT ["python", "app.py"]