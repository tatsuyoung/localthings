
document.getElementById("comment").style.visibility = "hidden";
    function clickBtn2(){
        const comment = document.getElementById("comment");
        if(comment.style.visibility == "visible"){
        comment.style.visibility = "hidden";
        }else{
            comment.style.visibility = "visible";
        };
    };
