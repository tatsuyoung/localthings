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
                      $('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                      }

                  });
                  return xhr;
              },
              type : $(this).attr('method'),
              url : $(this).attr('action'),
              data : formData,
              cache: false,
              processData : false,
              contentType : false,
              success : function(data){
                  alert('Uploaded successful!!!');
//                  location.href = 'http://127.0.0.1:8000';
                    location.href = 'https://localthings.herokuapp.com'
              }
          });
          return false;
          }
          $(function() {
              $('#form').submit(upload);
      });





