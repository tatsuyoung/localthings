document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('01');
    if (!input) return;
    input.addEventListener('change', function(e) {
        const preview = document.getElementById('preview');
        preview.innerHTML = '';
        for (const file of e.target.files) {
            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.style.height = '80px';
                img.src = URL.createObjectURL(file);
                preview.appendChild(img);
            }
        }
    });
});