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
                const formattedText = fullText.replace(/\n/g, '<br>');
                snippet.innerHTML = formattedText;
                snippet.dataset.expanded = 'true';
                if (readMoreLink) readMoreLink.textContent = '詳細ページへ';
            } else {
                snippet.innerHTML = snippetText;
                snippet.dataset.expanded = 'false';
                if (readMoreLink) readMoreLink.textContent = '続きを読む';
            }
        });

        // ✅ 初期化済みフラグを付けて、2重登録防止
        snippet.dataset.initialized = 'true';
    });
}

// ✅ 初回DOM読み込み時に実行
document.addEventListener('DOMContentLoaded', function () {
    initializeFullText();
});