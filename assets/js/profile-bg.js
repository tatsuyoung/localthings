 $(function(){
        $("#id_bg").on('change', function(){
            var fileTwo = $(this).prop('files')[0];
            if(!($(".filenameTwo").length)){
            console.log('hi there')
            $("#two").append('<span class="filenameTwo"></span>');
        }
        $("#input-label-bg").addClass('changed');
        $(".filenameTwo").html(fileTwo.name);
        });
    });