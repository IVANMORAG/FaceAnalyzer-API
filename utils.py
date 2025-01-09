import cv2
import mediapipe as mp
from PIL import Image, ImageEnhance
import numpy as np
import os
from deepface import DeepFace

# Inicializamos el modelo de detección de rostros de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

def process_image(image_path):
    # Leer la imagen
    image = cv2.imread(image_path)
    
    # Convertir a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Convertir la imagen en escala de grises a BGR para poder dibujar en color
    gray_image_bgr = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    
    # Detectar los puntos faciales y dibujar las X
    points = detect_face_points(gray_image, gray_image_bgr)
    
    # Generar imágenes modificadas
    images = generate_modified_images(gray_image_bgr, points)
    
    # Detectar la emoción de la imagen
    emotion = detect_emotion(image)
    
    # Escribir la emoción solo en la imagen original
    images[0] = write_emotion_on_image(images[0], emotion)
    
    # Guardar las imágenes generadas en un buffer de memoria y devolverlas como bytes
    processed_images = []
    for idx, img in enumerate(images):
        img_byte_arr = image_to_bytes(img)
        processed_images.append(img_byte_arr)
    
    return {"message": "Imagen procesada", "images": processed_images}

def detect_face_points(gray_image, output_image):
    # Procesamos la imagen con MediaPipe
    results = face_mesh.process(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB))
    points = []
    
    # Índices específicos para ojos, cejas, nariz y labios (menos puntos)
    eye_indices = [33, 133, 362, 263]  # Ojos: arriba, abajo, izquierda, derecha
    eyebrow_indices = [70, 107, 336, 296]  # Cejas: izquierda y derecha de cada ceja
    nose_indices = [1, 197, 5]  # Nariz: centro, izquierda, derecha
    lips_indices = [13, 14, 78, 308]  # Labios: arriba, abajo, izquierda, derecha
    
    # Combina todos los índices relevantes (menos puntos que antes)
    relevant_indices = eye_indices + eyebrow_indices + nose_indices + lips_indices
    
    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            for idx, landmark in enumerate(landmarks.landmark):
                if idx in relevant_indices:  # Solo puntos relevantes
                    x = int(landmark.x * gray_image.shape[1])
                    y = int(landmark.y * gray_image.shape[0])
                    points.append((x, y))
                    
                    # Ajustamos el tamaño de la X basado en el tamaño de la imagen (más pequeña)
                    size = max(3, int(gray_image.shape[1] * 0.01))  # Tamaño más pequeño de la X
                    color = (0, 0, 255)  # Color rojo (BGR)
                    thickness = 1  # Grosor más delgado
                    # Líneas de la X (más pequeñas y delgadas)
                    cv2.line(output_image, (x - size, y - size), (x + size, y + size), color, thickness)
                    cv2.line(output_image, (x - size, y + size), (x + size, y - size), color, thickness)
    
    return points

def generate_modified_images(gray_image_bgr, points):
    images = []
    
    # Imagen original con puntos faciales
    images.append(gray_image_bgr)
    
    # Imagen girada 180 grados
    rotated = cv2.rotate(gray_image_bgr, cv2.ROTATE_180)
    images.append(rotated)
    
    # Imagen volteada horizontalmente (espejo)
    flipped = cv2.flip(gray_image_bgr, 1)
    images.append(flipped)
    
    # Imagen con brillo ajustado
    brightened = adjust_brightness(gray_image_bgr, 1.5)  # Incrementa el brillo en un 50%
    images.append(brightened)
    
    # Imagen corregida (alineada)
    aligned = cv2.warpAffine(gray_image_bgr, cv2.getRotationMatrix2D((gray_image_bgr.shape[1] / 2, gray_image_bgr.shape[0] / 2), 0, 1), (gray_image_bgr.shape[1], gray_image_bgr.shape[0]))
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

def detect_emotion(image):
    """Detecta la emoción en la imagen utilizando DeepFace."""
    analysis = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
    return analysis[0]['dominant_emotion']

def write_emotion_on_image(image, emotion):
    """Escribe la emoción en la imagen en un tamaño adecuado y centrado."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1  # Tamaño de la fuente
    thickness = 2  # Grosor de la fuente
    color = (0, 0, 0)  # Color negro
    (w, h), _ = cv2.getTextSize(emotion, font, font_scale, thickness)
    
    # Posicionar el texto en el centro
    x = int((image.shape[1] - w) / 2)
    y = int(image.shape[0] - 30)  # Ajustar para que esté cerca de la parte inferior
    
    # Añadir el texto a la imagen
    cv2.putText(image, emotion, (x, y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)
    
    return image
