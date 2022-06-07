$(document).ready(function(){

    $(document).on("click", ".notiList", function (){
        var num = $(this).attr("data-num");

        window.location.href = '/notice/viewer/'+num+'/' ;
    });

    $(document).on("click", ".pages", function (){
        var page = $(this).attr("data-page");

        window.location.href = "/notice/list/"+page+"/";
    });


});
