$(document).ready(function(){

    $(document).on("click", ".notiList", function (){
        var num = $(this).attr("data-num");
        var type = $(this).attr("data-type");

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/";
               return;
           } else {
               return;
           }
        }

        if( type == "notice" ) {
            window.location.href = '/lounge/notice/viewer/' + num + '/';
        }else if( type == "qa" ) {
            window.location.href = '/lounge/qanda/viewer/' + num + '/';
        }else if( type == "magazine" ) {
            window.location.href = '/lounge/magazine/viewer/' + num + '/';
        }else if( type == "bull" ) {
            window.location.href = '/lounge/bull/viewer/' + num + '/';
        }
    });


    $(document).on("click", ".mTtitle span, .audiVolunteer", function (e){
        e.preventDefault();
        e.stopPropagation();
        var type = $(this).attr("data-type");
        var num = $(this).attr("data-num");

        if( type == "notice" ){
            window.location.href = "/lounge/notice/list/1/";
        }else if( type == "qanda" ){
            window.location.href = "/lounge/qanda/list/1/";
        }else if( type == "magazine" ){
            window.location.href = "/lounge/magazine/list/1/";
        }else if( type == "bull" ){
            window.location.href = "/lounge/bull/list/1/";
        }

    });
});