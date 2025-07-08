function initializeSwipers() {
  document.querySelectorAll('.swiper-container').forEach(function (container) {
    if (container.dataset.initialized === 'true') return;

    const swiper = new Swiper(container, {
      loop: false,
      slidesPerView: 1,
      spaceBetween: 0,
      pagination: {
        el: container.querySelector('.swiper-pagination'),
        clickable: true,
      },
      navigation: {
        nextEl: container.querySelector('.swiper-button-next'),
        prevEl: container.querySelector('.swiper-button-prev'),
      },
      on: {
        init(swiperInstance) {
          updateNavVisibility(swiperInstance);
        },
        slideChange(swiperInstance) {
          updateNavVisibility(swiperInstance);

          // 前スライドのズーム解除
          const previousIndex = swiperInstance.previousIndex;
          const previousSlide = swiperInstance.slides[previousIndex];
          const previousImg = previousSlide?.querySelector('img');
          const previousZoomContainer = previousSlide?.querySelector('.swiper-zoom-container');

          if (previousImg) {
            previousImg.style.transform = 'none';
            previousImg.style.transition = 'transform 0.2s ease';
          }
          if (previousZoomContainer) {
            previousZoomContainer.scrollTop = 0;
            previousZoomContainer.scrollLeft = 0;
          }
        }
      }
    });

    function updateNavVisibility(swiperInstance) {
      const prevBtn = swiperInstance.params.navigation.prevEl;
      const nextBtn = swiperInstance.params.navigation.nextEl;
      if (prevBtn) prevBtn.style.display = swiperInstance.isBeginning ? 'none' : 'flex';
      if (nextBtn) nextBtn.style.display = swiperInstance.isEnd ? 'none' : 'flex';
    }

    // ✅ ここから追加：2本指ピンチでナビを非表示にする
    const prevBtn = container.querySelector('.swiper-button-prev');
    const nextBtn = container.querySelector('.swiper-button-next');
    const pagination = container.querySelector('.swiper-pagination');

    container.addEventListener('touchstart', function (e) {
      if (e.touches.length === 2) {
        if (prevBtn) prevBtn.style.display = 'none';
        if (nextBtn) nextBtn.style.display = 'none';
        if (pagination) pagination.style.display = 'none';
      }
    }, { passive: true });

    container.addEventListener('touchend', function (e) {
      if (e.touches.length < 2) {
        // スクロール終了後、ナビを復元
        updateNavVisibility(swiper);
        if (pagination) pagination.style.display = 'block';
      }
    }, { passive: true });

    container.dataset.initialized = 'true';
  });
}