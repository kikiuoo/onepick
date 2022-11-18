$(document).ready(function (){

      // Title 전체보기 클릭 이벤트 (Web 만 사용)
    $(document).on("click", ".mainTitle span", function(){
        var url = $(this).attr("data-url");

        window.location.href = url;
    });

    // 오디션 클릭 이벤트
    $(document).on("click", ".audition", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/?reUrl=/audi/audiDetail/actor/" + num + "/"
               return;
           } else {
                return;
           }
       }
       window.location.href = "/audi/audiDetail/actor/" + num + "/" //  ../audi/audiDetail/actor(기본값)/글번호/
    });

    $(document).on("click", ".audition .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/";
               return;
           } else {
                return;
           }
       }

        // 기업회원 픽기능 제한
        if( userType == "COMPAYN" ||  userType == "S-COMPANY" ){
           alert("해당 기능의 권한이 없습니다.") ;
           return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).parent().attr("data-num");

        updatePick("audition", nowType, num );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }

    });

    // 프로필 클릭 이벤트
    $(document).on("click", ".profile", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/?reUrl=/profile/profileDetail/actor/" + num + "/"
               return;
           } else {
                return;
           }
       }

       window.location.href = "/profile/profileDetail/actor/" + num + "/" //  ../profile/profDetail/글번호/
    });

    // 프로필 픽 기능. ( 구현 필요 )
    $(document).on("click", ".profile .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/";
               return;
           } else {
                return;
           }
       }

        // 일반회원 픽기능 제한
        if( userType == "NORMAL" ||  userType == "S-NORMAL" ){
           alert("해당 기능의 권한이 없습니다.") ;
           return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).parent().attr("data-num");

        updatePick("profile", nowType, num );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }
    });

    // 소베너 클릭이벤트
    $(document).on("click", ".subBanner", function(){
       var url = $(this).attr("data-url");

       window.location.href = url;
    });

    $(document).on("click", ".banner", function (){
        var url = $(this).attr("data-url");
        var num = $(this).attr("data-num");

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/"
               return;
           } else {
                return;
           }
       }

        updateCount(num);

        window.open(url);
    });


    $(document).on("click", ".exitBtn", function (){
        var num = $(this).attr("data-num");

        $("#popup_"+num).css("display", "none");
    });

    $(document).on("click", ".nonBtn", function (){
        var num = $(this).attr("data-num");
        var cookieName = "popupCookie_" + num;

        if($.cookie(cookieName) == undefined){
            //쿠키가 없는 경우 testCookie 쿠키를 추가
            $.cookie(cookieName, 'Y', { expires: 1, path: '/' });
        }

        $("#popup_"+num).css("display", "none");
    });

    $(document).on("click", ".popup .image", function (){
        var url = $(this).attr("data-url");

        window.open(url);
    });

    if(!$.cookie('popupCookie_1')){
        $("#popup_1").css("display", "block");
    }

    if(!$.cookie('popupCookie_2')){
        $("#popup_2").css("display", "block");
    }

});


function updateCount(num){
    $.ajax({
      url: "/ajax/updateBannerCount/",
      type: "GET",
      dataType: "json",
      data:{"num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });

}

function getIP(json){
    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ? true : false;

    var device = "";

    if(!isMobile) { device = "web";  } else { device = "mobile"; }

    $.ajax({
      url: "/ajax/updateCounting/",
      type: "GET",
      dataType: "json",
      data:{"ip" : json.ip, "device" : device},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });

}


function updatePick(tableName, nowType, num){
    $.ajax({
      url: "/ajax/updatePick/",
      type: "GET",
      dataType: "json",
      data:{"userID":userID, "tableName" : tableName, "nowType" : nowType, "num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });
}