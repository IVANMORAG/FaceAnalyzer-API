# Reconocimiento Facial con Flask

<a target="_blank" align="center">
  <img align="center" height="450" width="1000" alt="GIF" src="https://github.com/IVANMORAG/facial-point-detection/blob/main/recursos/Facial-Point-detector.gif">
</a>

<br>

## Descripción
Este proyecto es una aplicación web desarrollada con Flask que permite subir imágenes, procesarlas para detectar rostros, identificar puntos faciales, detectar emociones y aplicar transformaciones a las imágenes (como rotación, volteo y ajuste de brillo). Utiliza modelos preentrenados de TensorFlow/Keras para el reconocimiento facial y la detección de emociones, e integra ngrok para exponer el servidor local a internet.

## Características
- **Carga de Imágenes**: Los usuarios pueden subir imágenes a través de una interfaz web.
- **Procesamiento de Imágenes**:
  - Detección de rostros y puntos faciales usando Haar Cascade y un modelo de keypoints.
  - Detección de emociones (enojado, disgusto, miedo, feliz, triste, sorpresa, neutral).
  - Generación de imágenes modificadas (rotada, volteada, con brillo ajustado, alineada).
- **Historial de Imágenes**: Muestra un historial de imágenes subidas con opción de reprocesar o eliminar.
- **Integración con ngrok**: Permite exponer el servidor local a internet mediante un dominio personalizado.
- **Interfaz Web**: Interfaz responsive creada con HTML, CSS y JavaScript, con notificaciones usando SweetAlert2.

## Tecnologías Utilizadas
- **Backend**: Flask, Flask-CORS
- **Procesamiento de Imágenes**: OpenCV, PIL (Pillow)
- **Machine Learning**: TensorFlow/Keras (modelos preentrenados para keypoints y emociones)
- **Frontend**: HTML, CSS, JavaScript, SweetAlert2
- **Otros**: ngrok (para acceso público), UUID (para nombres únicos de archivos)

## Requisitos
- Python 3.8+
- ngrok instalado y configurado (con un dominio personalizado si se desea)
- Modelos preentrenados (`weights_keypoint.hdf5` y `weights_emotions.hdf5`) en la carpeta `models/`

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/reconocimiento-facial-flask.git
   cd reconocimiento-facial-flask
   ```

2. Crea y activa un entorno virtual:
    ```bash
    python -m venv mi_entorno
    source mi_entorno/bin/activate  # En Windows: mi_entorno\Scripts\activate
   ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Asegúrate de tener los modelos preentrenados en la carpeta models/.

5. Configura ngrok con tu dominio personalizado en app.py (variable NGROK_DOMAIN).

## Uso

1. Inicia la aplicación:
    ```bash
    pip install -r requirements.txt
    ```

2. ngrok iniciará automáticamente y mostrará la URL pública (por ejemplo, https://tu-dominio.ngrok-free.app).

3. Abre la URL en tu navegador para acceder a la interfaz web.

4. Sube una imagen, visualiza el historial, reprocesa o elimina imágenes según necesites.

## Estructura del Proyecto

```
reconocimiento-facial-flask/
│
├── app.py                   # Archivo principal de la aplicación Flask
├── utils.py                 # Funciones de procesamiento de imágenes
├── templates/
│   └── index.html           # Plantilla HTML para la interfaz web
├── static/
│   ├── css/
│   │   └── style.css        # Estilos CSS
│   └── js/
│       └── script.js        # Lógica JavaScript para la interfaz
├── imagenesCliente/         # Carpeta para almacenar imágenes subidas
├── processed_images/        # Carpeta para imágenes procesadas
├── models/                  # Carpeta para los modelos preentrenados (ignorada en .gitignore)
├── .gitignore               # Archivo para ignorar archivos innecesarios
└── README.md                # Documentación del proyecto
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:
Haz un fork del repositorio.

1. Crea una rama para tu feature (git checkout -b feature/nueva-funcionalidad).

2. Realiza tus cambios y haz commit (git commit -m "Añadir nueva funcionalidad").

3. Envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Autor

* Iván Mora
Creado en 2025 como proyecto de reconocimiento facial.

## Notas

* Asegúrate de tener suficiente espacio en disco para las carpetas de imágenes.

* Los modelos preentrenados no están incluidos en el repositorio; debes proporcionarlos.

* Si tienes problemas con ngrok, verifica tu configuración y conexión a internet.