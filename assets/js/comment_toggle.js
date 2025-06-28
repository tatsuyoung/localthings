document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggle-comment-button');
    const commentSection = document.getElementById('comment-section');

    toggleBtn.addEventListener('click', function () {
        if (commentSection.style.display === 'none') {
            commentSection.style.display = 'block';
            commentSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            commentSection.style.display = 'none';
        }
    });
});