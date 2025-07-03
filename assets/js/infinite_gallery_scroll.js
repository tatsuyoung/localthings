// static/js/infinite_gallery_scroll.js
document.addEventListener("DOMContentLoaded", function () {
    const galleryContainer = document.getElementById("gallery-container");
    const scrollTrigger = document.getElementById("scroll-trigger");
    const loader = document.getElementById("loader");
    const endMessage = loader.querySelector(".end-message");

    let currentPage = 1;
    let loading = false;

    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !loading) {
            loadMoreGallery();
        }
    });

    observer.observe(scrollTrigger);

    function loadMoreGallery() {
        loading = true;
        loader.style.display = "block";
        currentPage += 1;

        fetch(`/articles/gallery/?page=${currentPage}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => {
            if (!response.ok) throw new Error("Network error");
            return response.json();
        })
        .then(data => {
            galleryContainer.insertAdjacentHTML("beforeend", data.html);
            loading = false;
            loader.style.display = "none";

            if (!data.has_next) {
                observer.unobserve(scrollTrigger);
                endMessage.style.display = "block";
                scrollTrigger.remove();
            }
        })
        .catch(error => {
            console.error("読み込み中にエラーが発生しました:", error);
            loading = false;
            loader.style.display = "none";
        });
    }
});