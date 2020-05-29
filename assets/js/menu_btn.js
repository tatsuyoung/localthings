
const menuBtn = document.querySelector('.menu_btn');
let menuOpen = false;
menuBtn.addEventListener('click', () => {
    if(!menuOpen){
        menuBtn.classList.add('open');
        menuOpen = true;
    } else {
        menuBtn.classList.remove('open');
        menuOpen = false;
    }
})

/* open and hide / toggle on click */

function toggleSideBar(){
    document.getElementById('fixedNav').classList.toggle('active');
}

