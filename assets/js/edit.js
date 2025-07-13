document.addEventListener("DOMContentLoaded", function () {
    const fileBlocks = document.querySelectorAll(".file-upload-label");

    fileBlocks.forEach(block => {
        // ✅ aタグ（現在の画像リンク）を非表示
        const link = block.querySelector('a');
        if (link) {
            link.style.display = 'none';
        }

        // ✅ clear チェックボックスとそのラベルを非表示
        const clearCheckbox = block.querySelector('input[type="checkbox"][name$="-image-clear"]');
        if (clearCheckbox) {
            clearCheckbox.style.display = 'none';
            const clearLabel = block.querySelector(`label[for="${clearCheckbox.id}"]`);
            if (clearLabel) clearLabel.style.display = 'none';
        }

        // ✅ <br> タグも削除（高さ調整のため）
        const br = block.querySelector('br');
        if (br) br.remove();

        // ✅ 不要なTextNode（現在: 変更:）を除去（textNodeのみ）
        block.childNodes.forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                const text = node.textContent.trim();
                if (text.startsWith("現在:") || text.startsWith("変更:")) {
                    node.remove();
                }
            }
        });

        // ✅ custom-file-button は表示したまま
        // ✅ input[type=file] の透過処理（上にボタン重ねる用）
        const fileInput = block.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.style.position = 'absolute';
            fileInput.style.opacity = 0;
            fileInput.style.width = '100%';
            fileInput.style.height = '100%';
            fileInput.style.cursor = 'pointer';
        }

        const customBtn = block.querySelector('.custom-file-button');
        if (fileInput && customBtn) {
            customBtn.addEventListener('click', function (e) {
                e.preventDefault();
                fileInput.click();
            });
        }
    });
});
