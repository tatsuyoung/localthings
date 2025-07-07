document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    let isLoading = false;
    const loader = document.getElementById("loader");
    const scrollContainer = document.querySelector(".center-and-right");

    function loadMoreArticles() {
        if (isLoading) return;

        isLoading = true;
        loader.style.display = 'block';
        currentPage += 1;

        fetch(`?page=${currentPage}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.html) {
                const feed = document.querySelector(".following-feed");
                feed.insertAdjacentHTML("beforeend", data.html);
                reinitializeDynamicContent();
            }

            const spinner = document.querySelector('#loader .spinner');
            const endMessage = document.querySelector('#loader .end-message');

            if (!data.has_next) {
                scrollContainer.removeEventListener("scroll", handleScroll);
                if (spinner) spinner.style.display = 'none';
                if (endMessage) endMessage.style.display = 'block';
            } else {
                loader.style.display = 'none';
            }

            isLoading = false;
        })
        .catch(err => {
            console.error("記事の取得に失敗しました:", err);
            isLoading = false;
        });
    }

    function handleScroll() {
        if (scrollContainer.scrollTop + scrollContainer.clientHeight >= scrollContainer.scrollHeight - 300) {
            loadMoreArticles();
        }
    }

    scrollContainer.addEventListener("scroll", handleScroll);

    function reinitializeDynamicContent() {
        if (typeof initializeFullText === "function") {
            initializeFullText();
        }
        if (typeof initializeSwipers === 'function') {
            initializeSwipers();
        }
        if (typeof initializeCommentToggles === 'function') {
            initializeCommentToggles();
        }
        if (typeof initializeLikeButtons === 'function') {
            initializeLikeButtons();
        }
        if (typeof initializeBookmarkButtons === 'function') {
            initializeBookmarkButtons();
        }
        if (typeof initializeCommentForms === 'function') {
            initializeCommentForms(); 
        }
    }

    // ✅ 初回ロード時にも初期化
    reinitializeDynamicContent();
});