document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    let isLoading = false;
    const loader = document.getElementById("loader");

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
            }

            const spinner = document.querySelector('#loader .spinner');
            const endMessage = document.querySelector('#loader .end-message');

            if (!data.has_next) {
                window.removeEventListener("scroll", handleScroll);

                if (spinner) spinner.style.display = 'none';
                if (endMessage) endMessage.style.display = 'block';
                // ✅ loaderはそのまま表示
            } else {
                loader.style.display = 'none';  // ✅ 次があれば非表示
            }

            isLoading = false;
        })
        .catch(err => {
            console.error(err);
            isLoading = false;
        });
    }

    function handleScroll() {
        if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight - 300)) {
            loadMoreArticles();
        }
    }

    window.addEventListener("scroll", handleScroll);
});