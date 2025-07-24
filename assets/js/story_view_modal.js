function openStoryViewModal(userId) {
  fetch(`/stories/view/${userId}/`)
    .then(response => response.text())
    .then(html => {
      document.getElementById('storyViewModalBody').innerHTML = html;
      document.getElementById('storyViewModal').classList.remove('hidden');
    })
    .catch(err => {
      console.error(err);
      alert("ストーリーの表示に失敗しました。");
    });
}

function closeStoryViewModal() {
  document.getElementById('storyViewModal').classList.add('hidden');
  document.getElementById('storyViewModalBody').innerHTML = "";
}

document.querySelectorAll('.story-ring').forEach(storyRing => {
    storyRing.addEventListener('click', function () {
        const storyId = this.dataset.storyId;

        fetch(`/stories/mark_read/${storyId}/`, {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "ok") {
                this.classList.add("read");  // 即時反映
            }
        })
        .catch(error => {
            console.error("Fetchエラー:", error);
        });
    });
});