from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from utils import process_image  # Implementa correctamente esta función
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Crear carpeta 'processed_images' si no existe
processed_images_path = os.path.join(os.getcwd(), 'processed_images')
if not os.path.exists(processed_images_path):
    os.makedirs(processed_images_path)

# Configuración de carpetas
app.config['PROCESSED_IMAGES_FOLDER'] = processed_images_path

# Ruta para servir imágenes procesadas
@app.route('/processed_images/<filename>')
def send_processed_image(filename):
    return send_from_directory(app.config['PROCESSED_IMAGES_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar el envío de imágenes
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen"}), 400

    file = request.files['image']
    temp_file_path = os.path.join(app.config['PROCESSED_IMAGES_FOLDER'], 'uploaded_image.jpg')
    file.save(temp_file_path)

    # Procesar la imagen
    result = process_image(temp_file_path)

    # Guardar las imágenes procesadas
    processed_images = []
    for idx, img_data in enumerate(result["images"]):
        processed_image_path = os.path.join(app.config['PROCESSED_IMAGES_FOLDER'], f"processed_image_{idx}.jpg")
        with open(processed_image_path, "wb") as f:
            f.write(img_data)
        processed_images.append(f"/processed_images/processed_image_{idx}.jpg")

    return jsonify({"message": "Imágenes procesadas correctamente", "images": processed_images})

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
