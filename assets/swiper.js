var swiper = new Swiper('.swiper-container', {
      effect: 'coverflow',
      grabCursor: true,
      freeMode: true,
      spaceBetween: 0,
      centeredSlides: true,
      preventClicks:false,
      slidesPerView: 'auto',
      coverflowEffect: {
        rotate: 30,
        stretch: 0,
        depth: 500,
        modifier: 1,
        slideShadows : true,
      },
      pagination: {
        el: '.swiper-pagination',
      },
    });