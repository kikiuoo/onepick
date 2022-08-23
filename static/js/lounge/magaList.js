$(document).ready(function(){

    $(document).on("click", ".notiList", function (){
        var num = $(this).attr("data-num");

        if( userID == "" ){
            alert("로그인 후 이용 가능합니다.");
            return;
        }
        window.location.href = '/lounge/magazine/viewer/'+num+'/' ;
    });

    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
        var page = $(this).attr("data-page");

        window.location.href = "/lounge/magazine/list/"+page+"/";
    });

    $(document).on("click", ".addQandA", function (){
        if( userID == "" ){
            alert("로그인 후 이용 가능합니다.");
            return;
        }

        window.location.href = "/lounge/magazine/write/";
    });

});
