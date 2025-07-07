function initializeCommentForms() {
    document.querySelectorAll("form.comment-form").forEach(function (form) {
        // ✅ 二重登録を防止
        if (form.dataset.listenerAttached === 'true') return;

        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const formData   = new FormData(form);
            const action     = form.getAttribute("action");
            const articleId  = form.getAttribute("data-article-id");
            const commentList = document.querySelector(`#comment-list-${articleId}`);

            fetch(action, {
                method: "POST",
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                commentList.innerHTML = data.html;
                form.querySelector("textarea").value = "";
                scrollToBottom(articleId);
            })
            .catch(error => {
                console.error("Fetch error:", error);
                alert("投稿に失敗しました");
            });
        });

        // ✅ 登録済みフラグを立てる
        form.dataset.listenerAttached = 'true';
    });
}
// comment_post.js の末尾
document.addEventListener("DOMContentLoaded", function () {
    initializeCommentForms();
});
