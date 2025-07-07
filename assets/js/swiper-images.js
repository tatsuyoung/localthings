function initializeSwipers() {
    document.querySelectorAll('.swiper-container').forEach(function (container) {
        if (container.dataset.initialized === 'true') return;

        const swiper = new Swiper(container, {
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
            if (prevBtn) prevBtn.style.display = swiperInstance.isBeginning ? 'none' : 'flex';
            if (nextBtn) nextBtn.style.display = swiperInstance.isEnd ? 'none' : 'flex';
        }

        // ✅ ピンチズーム制御
        let isZooming = false;
        const prevBtn = container.querySelector('.swiper-button-prev');
        const nextBtn = container.querySelector('.swiper-button-next');
        const pagination = container.querySelector('.swiper-pagination');

        container.addEventListener('touchstart', function (e) {
            if (e.touches.length === 2) {
                isZooming = true;
                swiper.allowTouchMove = false;
                if (prevBtn) prevBtn.style.display = 'none';
                if (nextBtn) nextBtn.style.display = 'none';
                if (pagination) pagination.style.display = 'none';
            }
        }, { passive: true });

        container.addEventListener('touchend', function (e) {
            if (isZooming && e.touches.length < 2) {
                isZooming = false;
                swiper.allowTouchMove = true;
                updateNavVisibility(swiper);
                if (pagination) pagination.style.display = 'block';
            }
        }, { passive: true });

        container.dataset.initialized = 'true';
    });
}
