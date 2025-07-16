function convertHashtagsToLinks(text) {
    return text.replace(/#([^\s#]+)/g, function (match, tag) {
        return `<a href="/articles/tags/${encodeURIComponent(tag)}/" class="hashtag-link">#${tag}</a>`;
    });
}

function initializeFullText() {
    const snippets = document.querySelectorAll('.snippet-text');

    snippets.forEach(snippet => {
        // すでに初期化されているならスキップ
        if (snippet.dataset.initialized === 'true') return;

        const fullText = snippet.dataset.fulltext;
        const snippetText = snippet.dataset.snippet;
        const readMoreLink = snippet.parentElement.querySelector('.read-more');

        snippet.addEventListener('click', function () {
            const isExpanded = snippet.dataset.expanded === 'true';

            if (!isExpanded) {
                // ✅ 改行＋ハッシュタグ処理
                const formattedText = convertHashtagsToLinks(fullText).replace(/\n/g, '<br>');
                snippet.innerHTML = formattedText;
                snippet.dataset.expanded = 'true';
                if (readMoreLink) readMoreLink.textContent = '詳細ページへ';
            } else {
                snippet.innerHTML = snippetText;
                snippet.dataset.expanded = 'false';
                if (readMoreLink) readMoreLink.textContent = '続きを読む';
            }
        });

        snippet.dataset.initialized = 'true';
    });
}

document.addEventListener('DOMContentLoaded', function () {
    initializeFullText();
});