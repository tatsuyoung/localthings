const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

function initializeLikeButtons() {
    document.querySelectorAll('.btn-like').forEach(button => {
        // ✅ 二重登録防止
        if (button.dataset.listenerAttached === 'true') return;

        button.addEventListener('click', function(e) {
            e.preventDefault();

            const articleId = this.dataset.id;
            const title = this.dataset.title;
            const icon = this.querySelector('i');
            const likeCountElem = document.querySelector(`#like-count-${articleId}`);

            fetch(`/articles/like/${articleId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ 'title': title })
            })
            .then(response => {
                if (response.status === 403) {
                    alert("ログインしてください。");
                    throw new Error("403 Unauthorized");
                }
                if (!response.ok) {
                    throw new Error("Fetch error: " + response.status);
                }
                return response.json();
            })
            .then(data => {
                const iconItem = this.closest('li.icon-items');

                if (icon.classList.contains('fas')) {
                    icon.classList.replace('fas', 'far');
                    if (iconItem) iconItem.classList.remove('liked');
                } else {
                    icon.classList.replace('far', 'fas');
                    if (iconItem) iconItem.classList.add('liked');
                }

                if (likeCountElem) {
                    likeCountElem.textContent = data.likes_count;
                }
            })
            .catch(error => {
                if (error.message !== "403 Unauthorized") {
                    alert("エラーが発生しました");
                    console.error(error);
                }
            });
        });

        // ✅ フラグをつけて再登録を防ぐ
        button.dataset.listenerAttached = 'true';
    });
}

// 初回のみ自動実行
document.addEventListener("DOMContentLoaded", function () {
    initializeLikeButtons();
});