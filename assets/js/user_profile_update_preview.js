document.addEventListener("DOMContentLoaded", function () {
    // アイコンプレビュー（これはそのままでOK）
    const iconInput = document.getElementById("id_image");
    const iconPreview = document.querySelector(".img-cover2");

    if (iconInput && iconPreview) {
        iconInput.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    iconPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 背景プレビュー（No-image対応）
    const bgInput = document.getElementById("id_bg");
    let bgPreview = document.querySelector(".profile-bg");

    if (bgInput) {
        bgInput.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                // プレビュー対象のimgタグがなければ作成
                if (!bgPreview) {
                    bgPreview = document.createElement("img");
                    bgPreview.className = "profile-bg";
                    bgPreview.alt = "background-img";
                    bgPreview.loading = "lazy";

                    // 差し込む場所を決める（例: 元のNo-image.pngのimgタグを置き換える）
                    const fallbackImg = document.querySelector('img[alt="No image"]');
                    if (fallbackImg && fallbackImg.parentNode) {
                        fallbackImg.parentNode.replaceChild(bgPreview, fallbackImg);
                    } else {
                        // それもなければ append（保険）
                        document.body.appendChild(bgPreview);
                    }
                }

                // プレビュー表示
                const reader = new FileReader();
                reader.onload = function (e) {
                    bgPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});