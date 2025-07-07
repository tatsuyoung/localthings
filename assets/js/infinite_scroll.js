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

                // ✅ 追加要素を挿入後に再初期化
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

    // ✅ Swiperとfulltextを再初期化する関数
    function reinitializeDynamicContent() {
        // Swiper 再初期化（未初期化のみに）
        document.querySelectorAll('.swiper-container').forEach(function (container) {
            if (!container.classList.contains('swiper-initialized')) {
                new Swiper(container, {
                    loop: false,
                    pagination: {
                        el: container.querySelector('.swiper-pagination'),
                        clickable: true,
                    },
                    navigation: {
                        nextEl: container.querySelector('.swiper-button-next'),
                        prevEl: container.querySelector('.swiper-button-prev'),
                    },
                    slidesPerView: 1,
                    spaceBetween: 0,
                    on: {
                        init: function () {
                            updateNavVisibility(this);
                        },
                        slideChange: function () {
                            updateNavVisibility(this);
                        }
                    }
                });

                function updateNavVisibility(swiperInstance) {
                    const prevBtn = swiperInstance.params.navigation.prevEl;
                    const nextBtn = swiperInstance.params.navigation.nextEl;

                    if (prevBtn) {
                        prevBtn.style.display = swiperInstance.isBeginning ? 'none' : 'flex';
                    }
                    if (nextBtn) {
                        nextBtn.style.display = swiperInstance.isEnd ? 'none' : 'flex';
                    }
                }
            }
        });

        // fulltext.js の関数が存在すれば呼び出す
        if (typeof initializeFullText === "function") {
            initializeFullText();
        }
        // swipers.jsの関数が存在すれば呼ぶ
        if (typeof initializeSwipers === 'function') {
            initializeSwipers();
        }
        // main_comment_toggle
        if (typeof initializeCommentToggles === 'function') {
            initializeCommentToggles();
        }
        // liked
        if (typeof initializeLikeButtons === 'function') {
            initializeLikeButtons();
        }
        // ブックマーク
        if (typeof initializeBookmarkButtons == 'function') {
            initializeBookmarkButtons();
        }
    }

    // ✅ 最初のDOM読み込み時にも実行（念のため）
    reinitializeDynamicContent();
});