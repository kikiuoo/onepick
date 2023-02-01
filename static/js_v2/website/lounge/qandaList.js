$(document).ready(function(){

    $(document).on("click", ".notiList", function (){
        var num = $(this).attr("data-num");

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href =  baseUrl + "login/local/?reUrl=/lounge/qanda/viewer/"+num+"/";
               return;
           } else {
               return;
           }
        }

        window.location.href =  baseUrl + 'lounge/qanda/viewer/'+num+'/' ;
    });

    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
        var page = $(this).attr("data-page");

        window.location.href =  baseUrl + "lounge/qanda/list/"+page+"/";
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

        window.location.href =  baseUrl + "lounge/qanda/write/";
    });

    $(document).on("click", "#myView", function (){
        var check = $('input:checkbox[id="myView"]').is(":checked") ;

        if( check == true ){
            window.location.href =  baseUrl + "lounge/qanda/myList/1/";
        }else{
            window.location.href =  baseUrl + "lounge/qanda/list/1/";
        }

    });


});
