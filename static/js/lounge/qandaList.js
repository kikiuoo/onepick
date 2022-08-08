$(document).ready(function(){

    $(document).on("click", ".notiList", function (){
        var num = $(this).attr("data-num");

        window.location.href = '/lounge/qanda/viewer/'+num+'/' ;
    });

    $(document).on("click", ".pages", function (){
        var page = $(this).attr("data-page");

        window.location.href = "/lounge/qanda/list/"+page+"/";
    });

    $(document).on("click", ".addQandA", function (){
       window.location.href = "/lounge/qanda/write/";
    });

    $(document).on("click", "#myView", function (){
        var check = $('input:checkbox[id="myView"]').is(":checked") ;

        if( check == true ){
            window.location.href = "/lounge/qanda/myList/1/";
        }else{
            window.location.href = "/lounge/qanda/list/1/";
        }

    });


});
