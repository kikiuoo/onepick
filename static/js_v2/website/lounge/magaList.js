$(document).ready(function(){

    $(document).on("click", ".notiList", function (){
        var num = $(this).attr("data-num");

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href =  baseUrl + "login/local/?reUrl=/lounge/magazine/viewer/"+num+"/";
               return;
           } else {
               return;
           }
        }

        window.location.href =  baseUrl + 'lounge/magazine/viewer/'+num+'/' ;
    });

    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
        var page = $(this).attr("data-page");

        window.location.href =  baseUrl + "lounge/magazine/list/"+page+"/";
    });

    $(document).on("click", ".addQandA", function (){
        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href =  baseUrl + "login/local/";
               return;
           } else {
               return;
           }
        }
        window.location.href =  baseUrl + "lounge/magazine/write/";
    });

});
