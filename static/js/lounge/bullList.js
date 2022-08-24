$(document).ready(function(){

    $(document).on("click", ".notiList", function (){
        var num = $(this).attr("data-num");

         if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/?reUrl=/lounge/bull/viewer/"+num+"/";
               return;
           } else {
               return;
           }
        }

        if( userID == "" ){
            alert("로그인 후 이용 가능합니다.");
            return;
        }

        window.location.href = '/lounge/bull/viewer/'+num+'/' ;
    });

    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
        var page = $(this).attr("data-page");

        window.location.href = "/lounge/bull/list/"+page+"/";
    });

    $(document).on("click", ".addQandA", function (){

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/?reUrl=/lounge/bull/list/1/";
               return;
           } else {
               return;
           }
        }

        window.location.href = "/lounge/bull/write/";
    });

});
