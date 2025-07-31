document.addEventListener('click', function (e) {
    const button = e.target.closest('.follow-button');
    if (!button) return;

    e.preventDefault();

    const username = button.dataset.username;
    const isFollowing = button.dataset.isFollowing === 'true';

    fetch('/accounts/follow/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: new URLSearchParams({ username })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const followText = button.querySelector('.follow-text');
            if (followText) {
                followText.textContent = data.is_following ? 'フォロー中' : 'フォロー';
            }
            button.dataset.isFollowing = data.is_following ? 'true' : 'false';
            button.classList.toggle('is-following', data.is_following);

            const followerEl  = document.querySelector(`.hover-profile-follow .followers-count[data-username="${username}"]`);
            const followingEl = document.querySelector(`.hover-profile-follow .following-count[data-username="${username}"]`);
            if (followerEl) followerEl.textContent = data.followers_count;
            if (followingEl) followingEl.textContent = data.following_count;

            const myFollowingCountEl = document.querySelector('#my-following-count');
            if (myFollowingCountEl && data.my_following_count !== undefined) {
                myFollowingCountEl.textContent = data.my_following_count;
            }
        }
    })
    .catch(err => console.error('Follow toggle failed:', err));
});

// DjangoのCSRFトークン取得用（Cookieから）
function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
    return cookieValue;
}