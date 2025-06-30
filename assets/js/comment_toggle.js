// 1. まず関数定義
function scrollToBottom(articleId) {
    const wrapper = document.getElementById(`comment-wrapper-${articleId}`);
    const scrollArea = wrapper?.querySelector('.comment-bg');
    if (scrollArea) {
        scrollArea.scrollTop = scrollArea.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const toggleBtns = document.querySelectorAll('.toggle-comment-btn');

    toggleBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const articleId = btn.getAttribute('data-article-id');
            const commentWrapper = document.getElementById(`comment-wrapper-${articleId}`);

            if (commentWrapper.style.display === 'none' || commentWrapper.style.display === '') {
                commentWrapper.style.display = 'block';
                commentWrapper.scrollIntoView({ behavior: 'smooth' });
                // ✅ コメントエリアが表示されたあとにスクロール
                setTimeout(() => scrollToBottom(articleId), 100); // DOMの描画後にスクロール
            } else {
                commentWrapper.style.display = 'none';
            }
        });
    });
});