// 1. スクロール関数
function scrollToBottom(articleId) {
    const wrapper = document.getElementById(`comment-wrapper-${articleId}`);
    const scrollArea = wrapper?.querySelector('.comment-bg');
    if (scrollArea) {
        scrollArea.scrollTop = scrollArea.scrollHeight;
    }
}

// 2. コメントボタン初期化処理を関数化（再実行できるように）
function initializeCommentToggles() {
    document.querySelectorAll('.toggle-comment-btn').forEach(function (btn) {
        // ✅ 二重登録を防ぐため、既に登録済みならスキップ
        if (btn.dataset.listenerAttached === 'true') return;

        btn.addEventListener('click', function () {
            const articleId = btn.getAttribute('data-article-id');
            const commentWrapper = document.getElementById(`comment-wrapper-${articleId}`);

            if (commentWrapper.style.display === 'none' || commentWrapper.style.display === '') {
                commentWrapper.style.display = 'block';
                commentWrapper.scrollIntoView({ behavior: 'smooth' });
                setTimeout(() => scrollToBottom(articleId), 100);
            } else {
                commentWrapper.style.display = 'none';
            }
        });

        // ✅ フラグ追加で2回目の登録防止
        btn.dataset.listenerAttached = 'true';
    });
}

// 3. 初期化
document.addEventListener('DOMContentLoaded', function () {
    initializeCommentToggles();
});