const nav = document.getElementById("nav");
const scrollUp   = "scroll-up";
const scrollDown = "scroll-down";
let lastScroll = 0;

// 初期状態を scroll-up に
nav.classList.add(scrollUp);

window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll === 0) {
        nav.classList.remove(scrollUp);
        nav.classList.remove(scrollDown);
        return;
    }

    if (currentScroll > lastScroll && !nav.classList.contains(scrollDown)) {
        // 下にスクロール → ナビ非表示
        nav.classList.remove(scrollUp);
        nav.classList.add(scrollDown);
    } else if (currentScroll < lastScroll && nav.classList.contains(scrollDown)) {
        // 上にスクロール → ナビ再表示
        nav.classList.remove(scrollDown);
        nav.classList.add(scrollUp);
    }

    lastScroll = currentScroll;
});