$(document).ready(function(){

    $("#search").val(word);

    $(document).on("click", ".cate", function (){
        var url = $(this).attr("data-url");

        window.location.href = url;
    });

    $(document).on("click", ".audition, .audiListBox", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
            alert("로그인 후 이용가능합니다.");
            //return;
       }

       window.open( '/audi/audiDetail/all/' +num +"/" );
    });

});