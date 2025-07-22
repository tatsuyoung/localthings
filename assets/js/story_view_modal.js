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