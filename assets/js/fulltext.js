document.addEventListener('DOMContentLoaded', function () {
    const snippets = document.querySelectorAll('.snippet-text');

    snippets.forEach(snippet => {
        const fullText = snippet.dataset.fulltext;
        const snippetText = snippet.dataset.snippet;

        snippet.addEventListener('click', function () {
            const isExpanded = snippet.dataset.expanded === 'true';

            if (!isExpanded) {
                snippet.innerText = fullText;
                snippet.dataset.expanded = 'true';
            } else {
                snippet.innerText = snippetText;
                snippet.dataset.expanded = 'false';
            }
        });
    });
});