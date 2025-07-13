document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('01');
    if (!input) return;

    input.addEventListener('change', function(e) {
        const preview = document.getElementById('preview');
        preview.innerHTML = '';

        const files = Array.from(e.target.files);

        if (files.length > 5) {
            alert("最大5枚までアップロードできます。");
            input.value = '';  // 入力をクリア
            return;
        }

        files.forEach(file => {
            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.classList.add("preview-img");
                img.src = URL.createObjectURL(file);
                preview.appendChild(img);
            }
        });
    });
});