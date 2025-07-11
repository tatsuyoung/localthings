document.addEventListener("DOMContentLoaded", function () {
    // ✅ CSRFトークン取得関数（共通利用可）
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ✅ 初期化関数：infinite scrollで読み込まれたブックマークボタンにも対応
    window.initializeBookmarkButtons = function () {
        const bookmarkButtons = document.querySelectorAll(".btn-book_mark");

        bookmarkButtons.forEach(function (button) {
            if (button.dataset.listenerAttached === 'true') return;

            button.addEventListener("click", function (e) {
                e.preventDefault();

                const articleId = this.dataset.id;
                const icon = this.querySelector("i");

                fetch(`/articles/book_mark/${articleId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                .then((res) => {
                    // ✅ ステータスがエラーならメッセージ取得を試みる
                    if (!res.ok) {
                        return res.json().then((data) => {
                            throw new Error(data.message || "エラーが発生しました");
                        });
                    }
                    return res.json();  // 正常時
                })
                .then((data) => {
                    icon.classList.toggle("fas");
                    icon.classList.toggle("far");
                })
                .catch((error) => {
                    console.error("ブックマーク処理中にエラー:", error);
                    alert(error.message); 
                }); 
            });

            button.dataset.listenerAttached = 'true';
        });
    };

    // ✅ 初回ロード時に実行
    initializeBookmarkButtons();
});