document.addEventListener("DOMContentLoaded", function() {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    document.querySelectorAll('.btn-like').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const articleId = this.dataset.id;
            const title = this.dataset.title;
            const icon = this.querySelector('i');
            const likeCountElem = this.closest('.heart-circle').querySelector('.like-count');

            fetch(`/articles/like/${articleId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'title': title
                })
            })
            .then(response => {
                if (response.status === 403) {
                    alert("ログインしてください。");
                    // ログインページに飛ばしたい場合はこちらも使えます：
                    // window.location.href = "/accounts/login/?next=" + window.location.pathname;
                    throw new Error("403 Unauthorized");
                }
                if (!response.ok) {
                    throw new Error("Fetch error: " + response.status);
                }
                return response.json();
            })
            .then(data => {
                // アイコン切り替え
                const iconItem = this.closest('li.icon-items');

                if (icon.classList.contains('fas')) {
                    icon.classList.remove('fas');
                    icon.classList.add('far');

                    // ✅ liked クラスも外す
                    if (iconItem) {
                        iconItem.classList.remove('liked');
                    }
                } else {
                    icon.classList.remove('far');
                    icon.classList.add('fas');

                    // ✅ liked クラスを追加
                    if (iconItem) {
                        iconItem.classList.add('liked');
                    }
                }

                // カウント更新
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
    });
});