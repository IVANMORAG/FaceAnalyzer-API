import cv2
import dlib
from PIL import Image, ImageEnhance
import numpy as np
import os
import io

# Inicializamos el detector de rostros de dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Configurar la carpeta para guardar las imágenes procesadas (aunque no las vamos a guardar en disco)
processed_images_path = os.path.join(os.getcwd(), 'processed_images')
if not os.path.exists(processed_images_path):
    os.makedirs(processed_images_path)

def process_image(image_path):
    # Leer la imagen
    image = cv2.imread(image_path)
    
    # Convertir a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detectar los puntos faciales
    points = detect_face_points(gray_image)
    
    # Generar imágenes modificadas
    images = generate_modified_images(gray_image, points)

    # Guardar las imágenes generadas en un buffer de memoria y devolverlas como bytes
    processed_images = []
    for idx, img in enumerate(images):
        # Convertir cada imagen a bytes en lugar de guardarla como archivo
        img_byte_arr = image_to_bytes(img)
        processed_images.append(img_byte_arr)

    return {"message": "Imagen procesada", "images": processed_images}

def detect_face_points(gray_image):
    faces = detector(gray_image)
    points = []

    for face in faces:
        shape = predictor(gray_image, face)
        for idx, pt in enumerate(shape.parts()):
            points.append((pt.x, pt.y))  # Guardamos los puntos faciales
            cv2.circle(gray_image, (pt.x, pt.y), 1, (0, 0, 255), -1)  # Marca los puntos faciales
    
    return points

def generate_modified_images(gray_image, points):
    images = []
    
    # Imagen original con puntos faciales
    images.append(gray_image)

    # Imagen girada 180 grados
    rotated = cv2.rotate(gray_image, cv2.ROTATE_180)
    images.append(rotated)

    # Imagen volteada horizontalmente (espejo)
    flipped = cv2.flip(gray_image, 1)
    images.append(flipped)

    # Imagen con brillo ajustado
    brightened = adjust_brightness(gray_image, 1.5)  # Incrementa el brillo en un 50%
    images.append(brightened)

    # Imagen corregida (alineada)
    aligned = cv2.warpAffine(gray_image, cv2.getRotationMatrix2D((gray_image.shape[1] / 2, gray_image.shape[0] / 2), 0, 1), (gray_image.shape[1], gray_image.shape[0]))
    images.append(aligned)
    
    return images

def adjust_brightness(image, factor):
    pil_image = Image.fromarray(image)
    enhancer = ImageEnhance.Brightness(pil_image)
    bright_image = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(bright_image), cv2.COLOR_RGB2BGR)

def image_to_bytes(image):
    """Convierte una imagen en un objeto de tipo bytes."""
    is_success, img_encoded = cv2.imencode('.jpg', image)  # Codificar la imagen como JPEG
    if is_success:
        return img_encoded.tobytes()  # Convertir a bytes
    else:
        return None
