function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}

const myCsrfToken = getCookie('csrftoken');


$("#form").submit(function(e) {
    e.preventDefault();

    const $animation = $("#fake-upload-animation");
    const $bar = $("#fake-bar");
    const $message = $("#fake-message");

    // Reset
    $animation.show();
    $bar.css({
        "width": "0%",
        "background": "linear-gradient(90deg, #4caf50, #81c784)"
    });

    $message
        .hide()
        .removeClass("error")
        .text("");

    // Fake progress
    let fakePercent = 0;

    const fakeInterval = setInterval(function() {

        if (fakePercent < 95) {
            fakePercent += Math.random() * 5;
            fakePercent = Math.min(fakePercent, 95);

            $bar.css("width", fakePercent + "%");
        }

    }, 200);


    // FormData
    const formData = new FormData(this);


    $.ajax({
        url: $("#form").attr("action"),
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            "X-CSRFToken": myCsrfToken
        },

        success: function(data) {

            clearInterval(fakeInterval);

            // Finish progress
            $bar.css("width", "100%");

            // Success messageは表示しない
            setTimeout(function() {
                $animation.hide();
                window.location.href = "/";

            }, 300);
        },


        error: function(xhr, status, error) {

            clearInterval(fakeInterval);

            // Barをエラー色に変更
            $bar.css({
                "width": "100%",
                "background": "#dc3545"
            });

            // Error messageだけ表示
            let message = "Upload failed.";

            if (xhr.responseJSON && xhr.responseJSON.error) {
                message = xhr.responseJSON.error;
            } else if (error) {
                message = "Error: " + error;
            }

            $message
                .text(message)
                .addClass("error")
                .show();
        }
    });
});