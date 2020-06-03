const pageTopBtn = document.getElementById('scroll-top');
    pageTopBtn.addEventListener("click", function(){
        const me = arguments.callee;
        const nowY = window.pageYOffset;
        window.scrollTo(0, Math.floor(nowY * 0.8)); //default 0.8
        if (nowY > 0){
            window.setTimeout(me, 10)
        }
    });