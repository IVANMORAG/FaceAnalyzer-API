// static/js/script.js
const form = document.getElementById('uploadForm');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', document.getElementById('image').files[0]);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    if (result.images) {
        document.getElementById('originalImage').src = result.images[0];

        const processedImagesDiv = document.getElementById('processedImages');
        processedImagesDiv.innerHTML = '';
        result.images.slice(1).forEach(img => {
            const imgElement = document.createElement('img');
            imgElement.src = img;
            imgElement.style.maxWidth = '100%';
            processedImagesDiv.appendChild(imgElement);
        });
    }
});
