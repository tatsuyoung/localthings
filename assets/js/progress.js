function upload(event) {
    event.preventDefault();
    var formData = new FormData($('#form').get(0));

    $.ajax({
        xhr : function(){
        var xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener('progress', function(e){
            if (e.lengthComputable){
                console.log('Bytes Loaded: ' + e.loaded);
                console.log('Total Size: ' + e.total);
                console.log('Percentage Uploaded: ' + (e.loaded / e.total))
                var percent = Math.round((e.loaded / e.total) * 100);
                $('.progress-bar').text(percent + '%');
                $('.progress-bar').css('width', percent + '%');
                }
            });
            return xhr;
        },
        type : $(this).attr('method'),
        url  : $(this).attr('action'),
        data : formData,
        cache: false,
        processData : false,
        contentType : false,
        success : function(data){
            alert('Uploaded successful!!!');
            location.href = '/';
        }
    });
    return false;
    }
    $(function() {
        $('#form').submit(upload);
});









