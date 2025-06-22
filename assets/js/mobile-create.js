document.addEventListener('DOMContentLoaded', function () {
    const circle = document.querySelector('.mobile-create-circle');
    let lastScrollTop = window.scrollY;
    let currentOpacity = 1;

    window.addEventListener('scroll', function () {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {
            // 下にスクロール → 薄く（0.3まで）
            currentOpacity = Math.max(currentOpacity - 0.05, 0.3);
        } else if (scrollTop < lastScrollTop) {
            // 上にスクロール → 濃く（1.0まで）
            currentOpacity = Math.min(currentOpacity + 0.05, 1.0);
        }

        circle.style.opacity = currentOpacity.toFixed(2);
        lastScrollTop = scrollTop;
    });
});