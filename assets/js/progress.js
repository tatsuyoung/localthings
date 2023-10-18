console.log("hello Progress")

function upload(e) {
    e.preventDefault();
    var formData = new FormData($("#form").get(0))

    $.ajax({
        xhr: function () {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', function (evt) {
                if (evt.lengthComputable) {
                    console.log('Bytes Loaded: ' + evt.loaded);
                    console.log('Total Size  : ' + evt.total);
                    console.log('Percentage Uploaded: ' + (evt.loaded / evt.total));
                    const percent = Math.round((evt.loaded / evt.total) * 100);
                    $("#progressBar").attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                }
            }, false);
            return xhr;
        },
        type: $("#form").attr('method'),
        url: $("#form").attr('action'),
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            alert('Uploaded successful!!!');
            location.href = '/';
        },
    });
    return false;
}

$(function () {
    $("#form").submit(upload);
});