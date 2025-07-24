document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 2;
    let isLoading = false;
    let hasNextPage = true;

    const container = document.getElementById("articleListContainer");
    const observerTarget = document.getElementById("scrollObserverTarget");
    const loader = document.getElementById("loader");
    const endMessage = document.querySelector(".end-message");
    const endMessageCircle = document.querySelector(".end-icon-wrapper");
    const tagSlug = container.dataset.tag;

    const articleIdsShown = new Set();  // 👈 表示済みIDを記録

    // 最初に表示されている記事IDも登録
    document.querySelectorAll(".hashtag-thumbnail").forEach(el => {
        const id = el.dataset.articleId;
        if (id) articleIdsShown.add(id);
    });

    const observer = new IntersectionObserver(callback, {
        root: document.querySelector(".center"),
        threshold: 1.0
    });

    if (observerTarget) {
        observer.observe(observerTarget);
    }

    function callback(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !isLoading && hasNextPage) {
                loadMore();
            }
        });
    }

    function loadMore() {
        if (isLoading || !hasNextPage) return;

        isLoading = true;
        loader.style.display = "block";

        fetch(`/articles/tags/${encodeURIComponent(tagSlug)}/?page=${currentPage}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            const tempDiv = document.createElement("div");
            tempDiv.innerHTML = data.html;

            // 👇 重複記事を除外して追加
            tempDiv.querySelectorAll(".hashtag-thumbnail").forEach(el => {
                const id = el.dataset.articleId;
                if (!articleIdsShown.has(id)) {
                    container.appendChild(el);
                    articleIdsShown.add(id);  // 👈 表示済みに追加
                }
            });

            Object.assign(articleData, data.article_data);

            if (data.has_next) {
                currentPage += 1;
                isLoading = false;
            } else {
                hasNextPage = false;
                loader.style.display = "none";
                endMessage.style.display = "block";
                endMessageCircle.style.display = "block";
            }
        })
        .catch(err => {
            console.error("読み込みエラー:", err);
            loader.style.display = "none";
            isLoading = false;
        });
    }
});