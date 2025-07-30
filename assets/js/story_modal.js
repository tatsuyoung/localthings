function openStoryModal() {
  document.getElementById("storyModal").classList.add("show");
}

function closeStoryModal() {
  document.getElementById("storyModal").classList.remove("show");
}
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closeStoryModal();
  }
});

function previewStory(input) {
  const preview = document.getElementById("preview");
  preview.innerHTML = "";

  const file = input.files[0];
  if (!file) return;

  const maxSizeMB = 50;
  if (file.size > maxSizeMB * 1024 * 1024) {
    alert(`ファイルサイズが大きすぎます（最大 ${maxSizeMB}MB まで）`);
    input.value = '';
    return;
  }

  const fileName = file.name.toLowerCase();
  const mimeType = file.type;
  const isMp4 = fileName.endsWith(".mp4") || mimeType === "video/mp4" || mimeType === "video/quicktime"; // iPhone MOV = quicktime

  if (!isMp4) {
    alert("MP4またはMOV形式の動画のみアップロードできます。");
    input.value = "";
    return;
  }

  const reader = new FileReader();
  reader.onload = function (e) {
    preview.innerHTML = `
      <video controls class="preview-video">
        <source src="${e.target.result}" type="${file.type}">
        お使いのブラウザはvideoタグに対応していません。
      </video>
    `;
  };
  reader.readAsDataURL(file);
}