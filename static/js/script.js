// static/js/script.js

// Función para cargar las imágenes previas subidas
async function cargarHistorial() {
    try {
        const response = await fetch('/historico_imagenes');
        
        if (!response.ok) {
            throw new Error('Error al cargar el historial de imágenes');
        }

        const result = await response.json();

        if (result.imagenes) {
            const historicoImagesDiv = document.getElementById('historicoImages');
            historicoImagesDiv.innerHTML = ''; // Limpiar el historial antes de agregar nuevas imágenes

            result.imagenes.forEach(imgUrl => {
                const imgElement = document.createElement('img');
                imgElement.src = imgUrl;
                imgElement.style.maxWidth = '100%';
                imgElement.style.cursor = 'pointer'; // Cambiar cursor para indicar que es clickeable
                imgElement.dataset.imageUrl = imgUrl; // Guardar la URL de la imagen como dato
                historicoImagesDiv.appendChild(imgElement);
            });
        }
    } catch (error) {
        console.error('Error al cargar las imágenes del historial:', error);
    }
}

// Delegar el evento de clic a un contenedor principal (historicoImages)
document.getElementById('historicoImages').addEventListener('click', (event) => {
    const imgElement = event.target;

    // Asegúrate de que el clic haya sido en una imagen
    if (imgElement.tagName === 'IMG' && imgElement.dataset.imageUrl) {
        reprocesarImagen(imgElement.dataset.imageUrl);
    }
});

// Función para reprocesar una imagen seleccionada del historial
async function reprocesarImagen(imageUrl) {
    try {
        const response = await fetch('/reprocesar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ imageUrl }),
        });

        if (!response.ok) {
            throw new Error('Error al reprocesar la imagen');
        }

        const result = await response.json();

        if (result.images) {
            document.getElementById('originalImage').src = imageUrl + '?t=' + new Date().getTime(); // Cache busting

            const processedImagesDiv = document.getElementById('processedImages');
            processedImagesDiv.innerHTML = ''; // Limpiar imágenes procesadas

            result.images.forEach(img => {
                const imgElement = document.createElement('img');
                imgElement.src = img + '?t=' + new Date().getTime(); // Cache busting
                imgElement.style.maxWidth = '100%';
                processedImagesDiv.appendChild(imgElement);
            });
        }
    } catch (error) {
        console.error('Error al reprocesar la imagen:', error);
    }
}

// Llamar a cargarHistorial cuando la página se cargue
window.onload = cargarHistorial;

// Lógica para subir la nueva imagen
const form = document.getElementById('uploadForm');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', document.getElementById('image').files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Error al subir la imagen');
        }

        const result = await response.json();

        if (result.images) {
            document.getElementById('originalImage').src = result.images[0] + '?t=' + new Date().getTime(); // Cache busting

            const processedImagesDiv = document.getElementById('processedImages');
            processedImagesDiv.innerHTML = ''; // Limpiar imágenes procesadas

            result.images.slice(1).forEach(img => {
                const imgElement = document.createElement('img');
                imgElement.src = img + '?t=' + new Date().getTime(); // Cache busting
                imgElement.style.maxWidth = '100%';
                processedImagesDiv.appendChild(imgElement);
            });

            // Volver a cargar el historial de imágenes para incluir la nueva
            cargarHistorial();
        }
    } catch (error) {
        console.error('Error al subir la imagen:', error);
    }
});
