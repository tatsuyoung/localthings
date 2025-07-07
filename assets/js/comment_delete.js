document.addEventListener("DOMContentLoaded", function () {
            // ✅ コメント削除（Ajax）
            function setDeleteHandlers() {
                document.querySelectorAll(".comment-delete-form").forEach(function (form) {
                    form.addEventListener("submit", function (e) {
                        e.preventDefault();
                        if (!confirm("このコメントを削除しますか？")) return;

                        const articleId = form.getAttribute("data-article-id");
                        const action = form.getAttribute("action");
                        const commentList = document.querySelector(`#comment-list-${articleId}`);

                        fetch(action, {
                            method: "POST",
                            headers: {
                                "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
                                "X-Requested-With": "XMLHttpRequest"
                            }
                        })
                        .then(response => response.json())
                        .then(data => {
                            commentList.innerHTML = data.html;
                            setDeleteHandlers();  // 🔁 再バインド
                        })
                        .catch(error => {
                            alert("削除に失敗しました");
                            console.error(error);
                        });
                    });
                });
            }

            setDeleteHandlers(); // 初期化時も実行
        });