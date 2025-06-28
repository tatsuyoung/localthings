document.addEventListener("DOMContentLoaded", function () {
    const expandables = document.querySelectorAll(".snippet-text.expandable");

    expandables.forEach(span => {
      let expanded = false;

      span.addEventListener("click", function () {
        const full = span.dataset.fulltext;
        const short = span.dataset.snippet;

        if (!expanded) {
          span.textContent = full;
        } else {
          span.textContent = short;
        }

        expanded = !expanded;
      });
    });
  });