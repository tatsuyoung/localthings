$(function(){
        $("#id_image").on('change',function(){
        var file = $(this).prop('files')[0];
        if(!($(".filename").length)){
        $("#input-group").append('<span class="filename"></span>');
     }
     $("#input-label").addClass('changed');
     $(".filename").html(file.name);
   });
 });