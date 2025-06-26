const pageTopBtn = document.getElementById('scroll-top');
pageTopBtn.addEventListener("click", function () {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});