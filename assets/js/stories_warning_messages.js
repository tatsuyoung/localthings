document.addEventListener("DOMContentLoaded", function () {
    if (typeof messages === "undefined") return;

    const toastContainer = document.getElementById("toast-container");

    messages.forEach(message => {
        const toast = document.createElement("div");
        toast.textContent = message.message;
        toast.className = `toast toast-${message.tags || 'info'}`;

        // スタイル
        toast.style.background = message.tags === 'error' ? '#e74c3c' :
                                 message.tags === 'success' ? '#2ecc71' :
                                 message.tags === 'warning' ? '#f39c12' : '#333';
        toast.style.color = "#fff";
        toast.style.padding = "10px 20px";
        toast.style.marginBottom = "10px";
        toast.style.borderRadius = "8px";
        toast.style.boxShadow = "0 2px 8px rgba(0,0,0,0.3)";
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.5s ease";

        toastContainer.appendChild(toast);

        // 表示
        setTimeout(() => toast.style.opacity = "1", 100);

        // 自動削除
        setTimeout(() => {
            toast.style.opacity = "0";
            setTimeout(() => toast.remove(), 500);
        }, 4000);
    });
});