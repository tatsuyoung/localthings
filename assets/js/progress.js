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
const myCsrfToken = getCookie('csrftoken');

$("#form").submit(function(e) {
    e.preventDefault();
    // const ok = confirm('Are you sure with the content of this article?');
    // if (!ok) return;

    // フェイクアニメーション開始
    $("#fake-upload-animation").show();
    let fakePercent = 0;
    $("#fake-bar").css("width", "0%");
    const fakeInterval = setInterval(function() {
        if (fakePercent < 95) { // 95%までゆっくり進める
            fakePercent += Math.random() * 5;
            $("#fake-bar").css("width", fakePercent + "%");
        }
    }, 200);

    // FormDataでフォーム内容を取得
    const formData = new FormData(this);

    $.ajax({
        url: $("#form").attr("action"),
        type: "POST",
        data: formData,
        processData: false, // これが重要
        contentType: false, // これが重要
        headers: {'X-CSRFToken': myCsrfToken},
        success: function (data) {
            clearInterval(fakeInterval);
            $("#fake-bar").css("width", "100%");
            $("#fake-message").text("Successfully uploaded!");
            setTimeout(function() {
                $("#fake-upload-animation").hide();
                window.location.href = "/";
            }, 800);
        },
        error: function (xhr, status, error) {
            clearInterval(fakeInterval);
            $("#fake-upload-animation").hide();
            alert("Error: " + error);
        }
    });
});