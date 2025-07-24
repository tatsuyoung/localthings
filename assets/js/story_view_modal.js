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

        // ✅ここを「既読記録用エンドポイント」に変更
        fetch(`/stories/mark_read/${storyId}/`, {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => {
            const contentType = response.headers.get("content-type");
            if (response.redirected || !contentType || !contentType.includes("application/json")) {
                throw new Error("ログインしていないか、JSONレスポンスではありません");
            }
            return response.json();
        })
        .then(data => {
            if (data && data.status === "ok") {
                this.classList.add("read");
            }
        })
        .catch(error => {
            console.error("Fetchエラー:", error);
        });
    });
});