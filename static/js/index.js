$(document).ready(function (){
    // 메인 베너 클릭 이벤트
    $(document).on("click", ".mainBanner", function (){
        // 추가 개발.
    });

    // Title 전체보기 클릭 이벤트 (Web 만 사용)
    $(document).on("click", ".mainTitle span", function(){
        var url = $(this).attr("data-url");

        window.location.href = url;
    });

    // 오디션 클릭 이벤트
    $(document).on("click", ".audition", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
            alert("로그인 후 이용가능합니다.");
            //return;
       }

       window.location.href = "/audi/audiDetail/actor/" + num + "/" //  ../audi/audiDetail/actor(기본값)/글번호/
    });

    $(document).on("click", ".audition .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
            alert("로그인 후 이용가능합니다.");
            return;
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
            alert("로그인 후 이용가능합니다.");
            //return;
       }
       window.location.href = "/profile/profileDetail/actor/" + num + "/" //  ../profile/profDetail/글번호/
    });

    // 프로필 픽 기능. ( 구현 필요 )
    $(document).on("click", ".profile .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        // 기능 구현 필요
        if( userID == ""){
            alert("로그인 후 이용가능합니다.");
            return;
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

});


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