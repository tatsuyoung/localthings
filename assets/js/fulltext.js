function convertHashtagsToLinks(text) {
    return text.replace(/#([^\s#]+)/g, function (match, tag) {
        return `<a href="/articles/tags/${encodeURIComponent(tag)}/" class="hashtag-link">#${tag}</a>`;
    });
}

function initializeFullText() {
  const wrappers = document.querySelectorAll('.snippet-wrapper');

  wrappers.forEach(wrapper => {
    const snippet = wrapper.querySelector('.snippet-text');

    if (snippet.dataset.initialized === 'true') return;

    const fullText = snippet.dataset.fulltext;
    const snippetText = snippet.dataset.snippet;
    const readMoreLink = wrapper.parentElement.querySelector('.read-more');

    wrapper.style.maxHeight = '80px';

    snippet.addEventListener('click', () => {
      const isExpanded = snippet.dataset.expanded === 'true';

      if (!isExpanded) {
        const formattedText = convertHashtagsToLinks(fullText).replace(/\n/g, '<br>');
        snippet.innerHTML = formattedText;

        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            const scrollHeight = snippet.scrollHeight;
            wrapper.style.maxHeight = scrollHeight + 'px';
            snippet.dataset.expanded = 'true';
            if (readMoreLink) readMoreLink.textContent = '詳細ページへ';
          });
        });
      } else {
        wrapper.style.maxHeight = '80px';
        snippet.dataset.expanded = 'false';

        setTimeout(() => {
          snippet.innerHTML = snippetText;
          if (readMoreLink) readMoreLink.textContent = '続きを読む';
        }, 100); // トランジション時間に合わせる
      }
    });

    snippet.dataset.initialized = 'true';
  });
}

document.addEventListener('DOMContentLoaded', function () {
    initializeFullText();
});