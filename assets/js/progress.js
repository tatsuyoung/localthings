// progress.js
// DjangoのCSRFトークン取得とAjaxへの設定
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // このcookieが目的のものか確認
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    headers: { "X-CSRFToken": csrftoken }
});

$(function () {
    $("#form").submit(function(e) {
        e.preventDefault(); // ← フォームのデフォルト送信を止める
        const ok = confirm('Are you sure with the content of this article?');
        if (!ok) return;

        const formData = new FormData($("#form").get(0));

        for (const [key, value] of formData.entries()) {
            console.log(key, value);
        }

        $.ajax({
            xhr: function () {
                const xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function (evt) {
                    console.log("progress event!!!!", evt);
                    if (evt.lengthComputable) {
                        const percent = Math.round((evt.loaded / evt.total) * 100);
                        $("#progressBar")
                            .attr("aria-valuenow", percent)
                            .css("width", percent + "%")
                            .text(percent + "%");
                    }
                }, false);
                xhr.addEventListener("readystatechange", function() {
                console.log("xhr readyState", xhr.readyState);
            });
            xhr.addEventListener("loadstart", function() {
                console.log("xhr loadstart");
            });
            xhr.addEventListener("loadend", function() {
                console.log("xhr loadend");
            });
            xhr.addEventListener("error", function() {
                console.log("xhr error");
            });
                return xhr;
            },
            type: $("#form").attr("method"),
            url: $("#form").attr("action"),
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                alert("Uploaded successfully!");
                window.location.href = "/";
            },
            error: function (xhr, status, error) {
                alert("Error: " + error);
            }
        });
    });
});
