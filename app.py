from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import uuid
import cv2
from utils import process_image  # Simulación de procesamiento
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Crear carpetas necesarias
imagenes_cliente_path = os.path.join(os.getcwd(), 'imagenesCliente')
if not os.path.exists(imagenes_cliente_path):
    os.makedirs(imagenes_cliente_path)

processed_images_path = os.path.join(os.getcwd(), 'processed_images')
if not os.path.exists(processed_images_path):
    os.makedirs(processed_images_path)

# Configuración de carpetas
app.config['IMAGENES_CLIENTE_FOLDER'] = imagenes_cliente_path
app.config['PROCESSED_IMAGES_FOLDER'] = processed_images_path

# Función para redimensionar imágenes grandes con OpenCV
def resize_image(image_path, max_width=800):
    """
    Redimensiona una imagen si su ancho es mayor que max_width.
    """
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    if width > max_width:
        aspect_ratio = height / width
        new_width = max_width
        new_height = int(new_width * aspect_ratio)
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(image_path, resized_img)

@app.route('/processed_images/<filename>')
def send_processed_image(filename):
    return send_from_directory(app.config['PROCESSED_IMAGES_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen"}), 400

    file = request.files['image']
    
    # Crear un nombre único para la imagen original
    unique_filename = f"{uuid.uuid4()}.jpg"
    temp_file_path = os.path.join(app.config['IMAGENES_CLIENTE_FOLDER'], unique_filename)
    
    # Guardar la imagen original temporalmente
    file.save(temp_file_path)

    # Redimensionar la imagen si es grande
    resize_image(temp_file_path)

    # Procesar la imagen
    result = process_image(temp_file_path)

    # Guardar las imágenes procesadas (sobrescribir siempre las mismas 4)
    processed_images = []
    for idx, img_data in enumerate(result["images"]):
        processed_image_name = f"processed_image_{idx}.jpg"
        processed_image_path = os.path.join(app.config['PROCESSED_IMAGES_FOLDER'], processed_image_name)
        
        # Sobrescribir el archivo procesado
        with open(processed_image_path, "wb") as f:
            f.write(img_data)
        
        processed_images.append(f"/processed_images/{processed_image_name}")

    return jsonify({"message": "Imágenes procesadas correctamente", "images": processed_images})

@app.route('/historico_imagenes')
def ver_historico():
    imagenes = os.listdir(app.config['IMAGENES_CLIENTE_FOLDER'])
    imagenes_urls = [f"/imagenesCliente/{img}" for img in imagenes if img.endswith('.jpg')]
    return jsonify({"imagenes": imagenes_urls})

@app.route('/imagenesCliente/<filename>')
def send_cliente_image(filename):
    return send_from_directory(app.config['IMAGENES_CLIENTE_FOLDER'], filename)

@app.route('/reprocesar', methods=['POST'])
def reprocesar_imagen():
    data = request.get_json()
    image_url = data.get('imageUrl')

    if not image_url:
        return jsonify({"error": "No se proporcionó ninguna imagen"}), 400

    image_name = os.path.basename(image_url)
    image_path = os.path.join(app.config['IMAGENES_CLIENTE_FOLDER'], image_name)

    if not os.path.exists(image_path):
        return jsonify({"error": "La imagen no existe"}), 404

    result = process_image(image_path)

    # Sobrescribir siempre las mismas imágenes procesadas
    processed_images = []
    for idx, img_data in enumerate(result["images"]):
        processed_image_name = f"processed_image_{idx}.jpg"
        processed_image_path = os.path.join(app.config['PROCESSED_IMAGES_FOLDER'], processed_image_name)
        
        with open(processed_image_path, "wb") as f:
            f.write(img_data)
        
        processed_images.append(f"/processed_images/{processed_image_name}")

    return jsonify({"message": "Imagen reprocesada correctamente", "images": processed_images})

# Ruta para eliminar una imagen
@app.route('/eliminar_imagen', methods=['POST'])
def eliminar_imagen():
    data = request.get_json()
    image_url = data.get('imageUrl')

    if not image_url:
        return jsonify({'success': False, 'message': 'No se proporcionó una URL de imagen'}), 400
    
    # Asumimos que la imagen está en la carpeta 'imagenesCliente'
    imagenes_cliente_path = os.path.join(app.config['IMAGENES_CLIENTE_FOLDER'], os.path.basename(image_url))

    # Verificar si la imagen existe
    if not os.path.exists(imagenes_cliente_path):
        return jsonify({'success': False, 'message': 'La imagen no existe en el servidor'}), 404

    try:
        # Eliminar el archivo
        os.remove(imagenes_cliente_path)
        return jsonify({'success': True, 'message': 'Imagen eliminada con éxito'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Ejecuta la aplicación Flask
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)