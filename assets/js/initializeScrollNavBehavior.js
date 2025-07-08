// ✅ スクロールに応じたナビゲーション制御
function initializeScrollNavBehavior() {
  const nav = document.querySelector(".mobile-nav");
  const scrollContainer = document.querySelector(".center-and-right");

  if (!nav || !scrollContainer) return;

  let lastScrollTop = scrollContainer.scrollTop;

  const newScrollHandler = () => {
    const scrollTop = scrollContainer.scrollTop;
    const delta = scrollTop - lastScrollTop;

    // 一番上：非表示
    if (scrollTop === 0) {
      nav.classList.remove("scrolled-up", "scrolled-down");
      nav.classList.add("nav-hidden");
    } else {
      nav.classList.remove("nav-hidden");

      if (delta > 5) {
        // 下スクロール → 半透明
        nav.classList.remove("scrolled-up");
        nav.classList.add("scrolled-down");
      } else if (delta < -5) {
        // 上スクロール → 完全表示
        nav.classList.remove("scrolled-down");
        nav.classList.add("scrolled-up");
      }
    }

    lastScrollTop = scrollTop;
  };

  scrollContainer.removeEventListener("scroll", scrollContainer._scrollNavHandler || (() => {}));
  scrollContainer._scrollNavHandler = newScrollHandler;
  scrollContainer.addEventListener("scroll", newScrollHandler);
}

// ✅ モバイル用作成ボタンの透過制御
function initializeMobileCreateOpacity() {
    const circle = document.querySelector('.mobile-create-circle');
    const scrollContainer = document.querySelector(".center-and-right");

    if (!circle || !scrollContainer) return;

    let lastScrollTop = scrollContainer.scrollTop;
    let currentOpacity = 1;

    const newOpacityHandler = () => {
        const scrollTop = scrollContainer.scrollTop;

        if (scrollTop > lastScrollTop) {
            currentOpacity = Math.max(currentOpacity - 0.05, 0.3);
        } else if (scrollTop < lastScrollTop) {
            currentOpacity = Math.min(currentOpacity + 0.05, 1.0);
        }

        circle.style.opacity = currentOpacity.toFixed(2);
        lastScrollTop = scrollTop;
    };

    scrollContainer.removeEventListener("scroll", scrollContainer._mobileOpacityHandler || (() => {}));
    scrollContainer._mobileOpacityHandler = newOpacityHandler;
    scrollContainer.addEventListener("scroll", newOpacityHandler);
}

// ✅ 他の機能とまとめて初期化（Infinite Scroll 時にも呼ばれる）
function reinitializeDynamicContent() {
    if (typeof initializeFullText === "function") initializeFullText();
    if (typeof initializeSwipers === "function") initializeSwipers();
    if (typeof initializeCommentToggles === "function") initializeCommentToggles();
    if (typeof initializeLikeButtons === "function") initializeLikeButtons();
    if (typeof initializeBookmarkButtons === "function") initializeBookmarkButtons();
    if (typeof initializeCommentForms === "function") initializeCommentForms();
    if (typeof initializeScrollNavBehavior === "function") initializeScrollNavBehavior();
    if (typeof initializeMobileCreateOpacity === "function") initializeMobileCreateOpacity();
}

// ✅ 初回読み込み時にも実行
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", reinitializeDynamicContent);
} else {
    reinitializeDynamicContent();
}