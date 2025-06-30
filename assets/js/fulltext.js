document.addEventListener('DOMContentLoaded', function () {
    const snippets = document.querySelectorAll('.snippet-text');

    snippets.forEach(snippet => {
        const fullText = snippet.dataset.fulltext;
        const snippetText = snippet.dataset.snippet;
        const detailUrl = snippet.dataset.detailUrl;

        const readMoreLink = snippet.parentElement.querySelector('.read-more');

        snippet.addEventListener('click', function () {
            const isExpanded = snippet.dataset.expanded === 'true';

            if (!isExpanded) {
                const formattedText = fullText.replace(/\n/g, '<br>');
                snippet.innerHTML = formattedText;
                snippet.dataset.expanded = 'true';

                // 「詳細ページへ」にテキスト変更
                readMoreLink.textContent = '詳細ページへ';
            } else {
                snippet.innerHTML = snippetText;
                snippet.dataset.expanded = 'false';

                // 元の「続きを読む」に戻す
                readMoreLink.textContent = '続きを読む';
            }
        });
    });
});