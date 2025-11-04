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

    const articleIdsShown = new Set();

    document.querySelectorAll(".hashtag-thumbnail").forEach(el => {
        const id = el.dataset.articleId;
        if (id) articleIdsShown.add(id);
    });

    // 🔹 callbackを先に定義
    function callback(entries) {
        entries.forEach(entry => {
            console.log("Observer callback triggered. isIntersecting:", entry.isIntersecting);
            console.log("isLoading:", isLoading, "hasNextPage:", hasNextPage);

            if (entry.isIntersecting && !isLoading && hasNextPage) {
                console.log("→ loadMore() 呼び出し");
                loadMore();
            }
        });
    }

    // 🔹 callback定義後にobserver作成
    const observer = new IntersectionObserver(callback, {
        root: null,
        rootMargin: "0px",
        threshold: 0.5
    });

    // 🔹 ターゲットが存在するか確認してからobserve
    if (observerTarget) {
        observer.observe(observerTarget);
        console.log("Observer is now observing:", observerTarget);
    } else {
        console.warn("#scrollObserverTarget not found");
    }

    // --- 以下 loadMore 定義 ---
    function loadMore() {
        if (isLoading || !hasNextPage) return;

        isLoading = true;
        loader.style.display = "block";

        fetch(`/articles/tags/${encodeURIComponent(tagSlug)}/?page=${currentPage}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Fetched data:", data);
            const tempDiv = document.createElement("div");
            tempDiv.innerHTML = data.html;

            tempDiv.querySelectorAll(".hashtag-thumbnail").forEach(el => {
                const id = el.dataset.articleId;
                if (!articleIdsShown.has(id)) {
                    container.appendChild(el);
                    articleIdsShown.add(id);
                }
            });

            if (data.has_next) {
                currentPage += 1;
            } else {
                hasNextPage = false;
                endMessage.style.display = "block";
                endMessageCircle.style.display = "block";
            }
        })
        .catch(err => {
            console.error("読み込みエラー:", err);
        })
        .finally(() => {
            loader.style.display = "none";
            isLoading = false;
        });
    }
});