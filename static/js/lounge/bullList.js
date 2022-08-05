$(document).ready(function(){

    $(document).on("click", ".notiList", function (){
        var num = $(this).attr("data-num");

        window.location.href = '/lounge/bull/viewer/'+num+'/' ;
    });

    $(document).on("click", ".pages", function (){
        var page = $(this).attr("data-page");

        window.location.href = "/lounge/bull/list/"+page+"/";
    });

    $(document).on("click", ".addQandA", function (){
       window.location.href = "/lounge/bull/write/";
    });

});
