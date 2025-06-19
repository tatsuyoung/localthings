
document.addEventListener("DOMContentLoaded", function() {
    const blocks = document.querySelectorAll(".article-image-form-block");

    blocks.forEach(block => {
        const childNodes = Array.from(block.childNodes);

        childNodes.forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                const text = node.textContent.trim();
                if (text.startsWith("現在:") || text.startsWith("変更:")) {
                    node.textContent = "";  // テキストだけ消す
                }
            }
        });

        // clear チェックボックスとそのラベルを非表示
        const clearCheckbox = block.querySelector('input[name$="-image-clear"]');
        const clearLabel = block.querySelector('label[for="' + clearCheckbox?.id + '"]');
        if (clearCheckbox) clearCheckbox.style.display = "none";
        if (clearLabel) clearLabel.style.display = "none";

        // "画像:" ラベルも非表示
        const fileLabel = block.querySelector('label[for^="id_images-"][for$="-image"]');
        if (fileLabel) fileLabel.style.display = "none";
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const blocks = document.querySelectorAll(".article-image-form-block");

    blocks.forEach(block => {
        const fileInput = block.querySelector('input[type="file"]');
        const customBtn = block.querySelector('.custom-file-button');

        if (fileInput && customBtn) {
            customBtn.addEventListener('click', () => fileInput.click());
        }

        // 不要なテキストや clear チェックボックスを非表示
        const childNodes = Array.from(block.childNodes);
        childNodes.forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                const text = node.textContent.trim();
                if (text.startsWith("現在:") || text.startsWith("変更:")) {
                    node.textContent = "";
                }
            }
        });

        const clearCheckbox = block.querySelector('input[name$="-image-clear"]');
        const clearLabel = block.querySelector('label[for="' + clearCheckbox?.id + '"]');
        if (clearCheckbox) clearCheckbox.style.display = "none";
        if (clearLabel) clearLabel.style.display = "none";

        const fileLabel = block.querySelector('label[for^="id_images-"][for$="-image"]');
        if (fileLabel) fileLabel.style.display = "none";
    });
});