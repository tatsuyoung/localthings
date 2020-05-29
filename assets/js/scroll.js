const nav = document.getElementById("nav");
const scrollUp = "scroll-up";
const scrollDown = "scroll-down";
let lastScroll = 0;

window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll == 0){
        nav.classList.remove(scrollUp);
        return;
    }

    if (currentScroll > lastScroll && !nav.classList.contains(scrollDown)){
        nav.classList.remove(scrollUp);
        nav.classList.add(scrollDown);
    } else if (currentScroll < lastScroll && nav.classList.contains(scrollDown)){
        nav.classList.remove(scrollDown);
        nav.classList.add(scrollUp);
    }
    lastScroll = currentScroll;
});