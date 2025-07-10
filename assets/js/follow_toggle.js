function initializeFollowButtons() {
    document.querySelectorAll('.follow-button').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const username = this.dataset.username;
            const isFollowing = this.dataset.isFollowing === 'true';

            fetch('/accounts/follow/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: new URLSearchParams({
                    username: username,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // ボタンテキストを切り替える
                    const followText = this.querySelector('.follow-text');
                    if (followText) {
                        followText.textContent = data.is_following ? 'フォロー中' : 'フォロー';
                    }
                    this.dataset.isFollowing = data.is_following ? 'true' : 'false';
                    // ✅ クラスの切り替え
                    this.classList.toggle('is-following', data.is_following);
                    // ✅ フォロワー数・フォロー中数を更新（該当要素があれば）
                    const followerEl  = document.querySelector(`.hover-profile-follow .followers-count[data-username="${username}"]`);
                    const followingEl = document.querySelector(`.hover-profile-follow .following-count[data-username="${username}"]`);

                    if (followerEl) followerEl.textContent = data.followers_count;
                    if (followingEl) followingEl.textContent = data.following_count;
                    // ✅ 自分自身の「フォロー中」数を更新（もし対象HTMLがあれば）
                    const myFollowingCountEl = document.querySelector('#my-following-count');
                    if (myFollowingCountEl && data.my_following_count !== undefined) {
                        myFollowingCountEl.textContent = data.my_following_count;
                    }
                }
            })
            .catch(err => console.error('Follow toggle failed:', err));
        });
    });
}

// DjangoのCSRFトークン取得用（Cookieから）
function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
    return cookieValue;
}