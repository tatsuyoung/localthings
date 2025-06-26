document.addEventListener("DOMContentLoaded", function () {
  const nav = document.querySelector(".mobile-nav");
  let lastScrollTop = 0;

  window.addEventListener("scroll", function () {
    let scrollTop = window.scrollY || document.documentElement.scrollTop;

    // スクロールが一番上に戻ったときは非表示
    if (scrollTop === 0) {
      nav.classList.remove("scrolled-up", "scrolled-down");
      nav.classList.add("nav-hidden");
      return;
    }

    // それ以外ならスクロール方向に応じてクラスを切り替え
    nav.classList.remove("nav-hidden");

    if (scrollTop > lastScrollTop) {
      // 下スクロール → 半透明
      nav.classList.remove("scrolled-up");
      nav.classList.add("scrolled-down");
    } else {
      // 上スクロール → 元に戻す
      nav.classList.remove("scrolled-down");
      nav.classList.add("scrolled-up");
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  });
});