import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
from tensorflow.keras.models import load_model

try:
    # Cargar los modelos preentrenados
    keypoints_model = load_model('models/weights_keypoint.hdf5')
    emotion_model = load_model('models/weights_emotions.hdf5')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
except Exception as e:
    print(f"Error al cargar los modelos: {str(e)}")
    raise

def process_image(image_path):
    try:
        # Verificar que la imagen existe
        if not os.path.exists(image_path):
            return {"message": "Imagen no encontrada", "images": []}
        
        # Leer la imagen
        image = cv2.imread(image_path)
        if image is None:
            return {"message": "Error al leer la imagen", "images": []}
        
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
        for img in images:
            img_bytes = image_to_bytes(img)
            if img_bytes is not None:
                processed_images.append(img_bytes)
        
        if not processed_images:
            return {"message": "Error al procesar las imágenes", "images": []}
        
        return {"message": "Imagen procesada", "images": processed_images}
    
    except Exception as e:
        print(f"Error en process_image: {str(e)}")
        return {"message": f"Error al procesar la imagen: {str(e)}", "images": []}

def detect_face_points(gray_image, output_image):
    try:
        # Ajustar solo los parámetros de detectMultiScale
        faces = face_cascade.detectMultiScale(gray_image, 
                                            scaleFactor=1.05,  # Ajustado de 1.1
                                            minNeighbors=5)    # Ajustado de 4
        points = []
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_img = gray_image[y:y+h, x:x+w]
            
            # Mantener el mismo preprocesamiento
            face_resized = cv2.resize(face_img, (96, 96))
            face_normalized = face_resized.astype('float32') / 255.0
            face_input = np.expand_dims(face_normalized, axis=0)
            
            # Predecir puntos faciales
            keypoints = keypoints_model.predict(face_input, verbose=0)[0]
            
            # Convertir predicciones a coordenadas
            for i in range(0, len(keypoints), 2):
                point_x = x + int(keypoints[i] * w / 96)
                point_y = y + int(keypoints[i+1] * h / 96)
                points.append((point_x, point_y))
                
                # Ajustar solo el tamaño de las X para mejor visualización
                size = max(3, int(min(w, h) * 0.015))
                color = (0, 0, 255)
                thickness = 1
                cv2.line(output_image, (point_x - size, point_y - size), 
                        (point_x + size, point_y + size), color, thickness)
                cv2.line(output_image, (point_x - size, point_y + size), 
                        (point_x + size, point_y - size), color, thickness)
        
        return points
    except Exception as e:
        print(f"Error en detect_face_points: {str(e)}")
        return []

def detect_emotion(image):
    try:
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (96, 96), interpolation=cv2.INTER_CUBIC)
            face_img = face_img.astype('float32') / 255.0
            face_img = np.expand_dims(face_img, axis=(0, -1))

            print(f"Dimensiones imagen procesada: {face_img.shape}")
            print(f"Valor máximo: {face_img.max()}, Valor mínimo: {face_img.min()}")

            prediction = emotion_model.predict(face_img, verbose=0)
            print(f"Predicción completa: {prediction}")
            
            predicted_emotion = emotions[np.argmax(prediction)]
            print(f"Emoción predicha: {predicted_emotion}")
            
            return predicted_emotion
        else:
            print("No se detectaron rostros en la imagen.")
            return 'neutral'
    except Exception as e:
        print(f"Error en detect_emotion: {str(e)}")
        return 'neutral'

def generate_modified_images(gray_image_bgr, points):
    try:
        images = []
        
        # Imagen original con puntos faciales
        images.append(gray_image_bgr.copy())
        
        # Imagen girada 180 grados
        rotated = cv2.rotate(gray_image_bgr.copy(), cv2.ROTATE_180)
        images.append(rotated)
        
        # Imagen volteada horizontalmente (espejo)
        flipped = cv2.flip(gray_image_bgr.copy(), 1)
        images.append(flipped)
        
        # Imagen con brillo ajustado
        brightened = adjust_brightness(gray_image_bgr.copy(), 1.5)
        images.append(brightened)
        
        # Imagen corregida (alineada)
        aligned = cv2.warpAffine(gray_image_bgr.copy(), 
                                cv2.getRotationMatrix2D((gray_image_bgr.shape[1] / 2, 
                                                       gray_image_bgr.shape[0] / 2), 0, 1), 
                                (gray_image_bgr.shape[1], gray_image_bgr.shape[0]))
        images.append(aligned)
        
        return images
    except Exception as e:
        print(f"Error en generate_modified_images: {str(e)}")
        return [gray_image_bgr.copy()] * 5  # Retorna 5 copias de la imagen original en caso de error

def adjust_brightness(image, factor):
    try:
        pil_image = Image.fromarray(image)
        enhancer = ImageEnhance.Brightness(pil_image)
        bright_image = enhancer.enhance(factor)
        return cv2.cvtColor(np.array(bright_image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error en adjust_brightness: {str(e)}")
        return image

def image_to_bytes(image):
    try:
        is_success, img_encoded = cv2.imencode('.jpg', image)
        if is_success:
            return img_encoded.tobytes()
        return None
    except Exception as e:
        print(f"Error en image_to_bytes: {str(e)}")
        return None

def write_emotion_on_image(image, emotion):
    try:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        color = (0, 0, 0)
        (w, h), _ = cv2.getTextSize(emotion, font, font_scale, thickness)
        
        x = int((image.shape[1] - w) / 2)
        y = int(image.shape[0] - 30)
        
        img_copy = image.copy()
        cv2.putText(img_copy, emotion, (x, y), font, font_scale, color, thickness, 
                    lineType=cv2.LINE_AA)
        
        return img_copy
    except Exception as e:
        print(f"Error en write_emotion_on_image: {str(e)}")
        return image