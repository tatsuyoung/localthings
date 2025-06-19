document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.swiper-container').forEach(function (container) {
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

            const isBeginning = swiperInstance.isBeginning;
            const isEnd = swiperInstance.isEnd;

            if (prevBtn) {
                prevBtn.style.display = isBeginning ? 'none' : 'flex';
            }
            if (nextBtn) {
                nextBtn.style.display = isEnd ? 'none' : 'flex';
            }
        }
    });
});
