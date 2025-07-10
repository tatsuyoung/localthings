function initializeHoverCard() {
    document.querySelectorAll('.hover-user-trigger').forEach(trigger => {
        const username = trigger.dataset.username;
        const card = document.querySelector(`.hover-profile-card[data-username="${username}"]`);
        if (!card) return;

        let hoverTimeout;

        function showCard() {
            clearTimeout(hoverTimeout);

            const rect = trigger.getBoundingClientRect();
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            const top  = rect.bottom + scrollTop + 20;
            const left = rect.left - 160;

            card.style.top = `${top}px`;
            card.style.left = `${left}px`;
            card.style.display = 'block';
        }

        function hideCard() {
            hoverTimeout = setTimeout(() => {
                card.style.display = 'none';
            }, 200); // ← 少し遅らせて非表示
        }

        if (window.innerWidth <= 768) return;

        // ✅ trigger も card も hover対象にする
        trigger.addEventListener('mouseenter', showCard);
        trigger.addEventListener('mouseleave', hideCard);
        card.addEventListener('mouseenter', () => clearTimeout(hoverTimeout));
        card.addEventListener('mouseleave', hideCard);
    });
}