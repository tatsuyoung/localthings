// 1. まず関数定義
function scrollToBottom(articleId) {
    const wrapper = document.getElementById(`comment-wrapper-${articleId}`);
    const scrollArea = wrapper?.querySelector('.comment-bg');
    if (scrollArea) {
        scrollArea.scrollTop = scrollArea.scrollHeight;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // 2. トグルボタンごとにイベントを付ける
    document.querySelectorAll('.toggle-comment-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const articleId = btn.getAttribute("data-article-id");
            const commentBox = document.getElementById("comment-wrapper-" + articleId);

            if (commentBox.style.display === "none" || commentBox.style.display === "") {
                commentBox.style.display = "block";
                commentBox.scrollIntoView({ behavior: "smooth" });

                // ✅ コメントエリアが表示されたあとにスクロール
                setTimeout(() => scrollToBottom(articleId), 100); // DOMの描画後にスクロール
            } else {
                commentBox.style.display = "none";
            }
        });
    });
});