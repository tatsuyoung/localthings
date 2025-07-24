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

  const reader = new FileReader();
  reader.onload = function (e) {
    if (file.type.startsWith("image/")) {
      preview.innerHTML = `<img src="${e.target.result}" class="preview-img" />`;
    } else if (file.type.startsWith("video/")) {
      preview.innerHTML = `
        <video controls class="preview-video">
          <source src="${e.target.result}" type="${file.type}">
          Your browser does not support the video tag.
        </video>
      `;
    }
  };
  reader.readAsDataURL(file);
}