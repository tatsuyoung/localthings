function initializeMobileCreateOpacity() {
    const circle = document.querySelector('.mobile-create-circle');
    const scrollContainer = document.querySelector(".center-and-right");

    if (!circle || !scrollContainer) return;

    // すでに初期化済みなら何もしない
    if (scrollContainer.dataset.opacityInitialized === "true") return;
    scrollContainer.dataset.opacityInitialized = "true";

    let lastScrollTop = scrollContainer.scrollTop;
    let currentOpacity = 1;

    scrollContainer.addEventListener('scroll', function () {
        const scrollTop = scrollContainer.scrollTop;

        if (scrollTop > lastScrollTop) {
            currentOpacity = Math.max(currentOpacity - 0.05, 0.3);
        } else if (scrollTop < lastScrollTop) {
            currentOpacity = Math.min(currentOpacity + 0.05, 1.0);
        }

        circle.style.opacity = currentOpacity.toFixed(2);
        lastScrollTop = scrollTop;
    });
}