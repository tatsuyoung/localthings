function initializeSwipers() {
    document.querySelectorAll('.swiper-container').forEach(function (container) {
        if (container.dataset.initialized === 'true') return;

        const swiper = new Swiper(container, {
            loop: false,
            slidesPerView: 1,
            spaceBetween: 0,

            // ✅ Zoom機能を有効化
            zoom: {
                maxRatio: 3,
            },

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
                },
                zoomChange(swiperInstance, scale) {
                    const prevBtn = swiperInstance.params.navigation.prevEl;
                    const nextBtn = swiperInstance.params.navigation.nextEl;
                    const pagination = swiperInstance.pagination.el;
                    const img = swiperInstance.slides[swiperInstance.activeIndex].querySelector('img');

                    if (scale > 1) {
                        swiperInstance.allowTouchMove = false;
                        if (prevBtn) prevBtn.style.display = 'none';
                        if (nextBtn) nextBtn.style.display = 'none';
                        if (pagination) pagination.style.display = 'none';
                    } else {
                        swiperInstance.allowTouchMove = true;
                        updateNavVisibility(swiperInstance);
                        if (pagination) pagination.style.display = 'block';
                        if (img) img.style.transform = 'none';  // ✅ transformリセット
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

        // ✅ pinch zoom 開始・終了時の overflow 制御
        const zoomContainer = container.querySelector('.swiper-zoom-container');

        container.addEventListener('touchstart', function (e) {
            if (e.touches.length === 2 && zoomContainer) {
                zoomContainer.style.overflow = 'auto'; // ✅ zoom中はスクロール可能に
            }
        }, { passive: true });

        container.addEventListener('touchend', function (e) {
            if (zoomContainer && e.touches.length < 2) {
                zoomContainer.style.overflow = 'auto'; // 必要に応じて 'hidden' に戻すことも可能
            }
        }, { passive: true });

        container.dataset.initialized = 'true';
    });
}