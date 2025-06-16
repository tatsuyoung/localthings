document.addEventListener("DOMContentLoaded", function() {
    function showUfo() {
        const ufo = document.getElementById('ufo');
        if (!ufo) return;
        ufo.classList.remove('ufo');
        // opacityで表示
        ufo.style.opacity = '1';
        // 再描画トリガー
        void ufo.offsetWidth;
        ufo.classList.add('ufo');
        setTimeout(() => {
            ufo.classList.remove('ufo');
            ufo.style.opacity = '0';
        }, 6000);
    }
    if (Math.random() < 0.3) {
        setTimeout(showUfo, 1000 + Math.random() * 3000);
    }
});