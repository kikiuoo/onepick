$(document).ready(function (){

    // 소셜 로그인 후 리다이렉트
    var reUrl = localStorage.getItem("reUrl");
    if ( reUrl != "" && reUrl != null ){
        localStorage.removeItem("reUrl");
        window.location.href = reUrl;
    }

      // Title 전체보기 클릭 이벤트 (Web 만 사용)
    $(document).on("click", ".mainTitle span", function(){
        var url = $(this).attr("data-url");

        window.location.href = url;
    });

    $(document).on("click", ".loungeList", function(){
       var num = $(this).attr("data-num");
       var type = $(this).attr("data-type");

       if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "login/local/?reUrl=/lounge/"+type+"/viewer/" + num + "/"
               return;
           } else {
                return;
           }
       }
       window.location.href = "/lounge/"+type+"/viewer/" + num + "/"
    });


    // 오디션 클릭 이벤트
    $(document).on("click", ".audition", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "login/local/?reUrl=/audi/audiDetail/actor/" + num + "/"
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
               window.location.href = "/login/local/";
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
    $(document).on("click", ".reComProfile, .comViewProfile, .miniProfile", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/login/local/?reUrl=/profile/profileDetail/actor/" + num + "/"
               return;
           } else {
                return;
           }
       }

       window.location.href = "/profile/profileDetail/actor/" + num + "/" //  ../profile/profDetail/글번호/
    });

    // 프로필 픽 기능. ( 구현 필요 )
    $(document).on("click", ".reComProfile .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/login/local/";
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
        var num = $(this).parent().parent().attr("data-num");
        var count = $(".pcNone .pickCounts_"+num).text();
        count *= 1;

        console.log(count);

        updatePick("profile", nowType, num );

         if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");

            $(".pickCounts_"+num).empty().text(count + 1);
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");

            $(".pickCounts_"+num).empty().text(count - 1);
        }
    });

    $(document).on("click", ".comViewProfile .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/login/local/";
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
        var num = $(this).parent().parent().attr("data-num");
        var count = $(".pickCounts_"+num).text();
        count *= 1;

        updatePick("profile", nowType, num );

         if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");

            $(".pickCounts_"+num).empty().text(count + 1);
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");

            $(".pickCounts_"+num).empty().text(count - 1);
        }
    });

    $(document).on("click", ".miniProfile .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/login/local/";
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
        var num = $(this).parent().parent().attr("data-num");

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

    $(document).on("click", ".mainBanner", function (){
        var url = $(this).attr("data-url");
        var num = $(this).attr("data-num");

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/login/local/"
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
        var type = $(this).attr("data-type");
        var cookieName = "popupCookie_" + num;

        if($.cookie(cookieName) == undefined){
            //쿠키가 없는 경우 testCookie 쿠키를 추가

            if ( type == "-99"){
                 $.cookie(cookieName, 'Y', { expires: 365, path: '/' });
            }else{
                 $.cookie(cookieName, 'Y', { expires: type*1, path: '/' });
            }

        }

        $("#popup_"+num).css("display", "none");
    });

    $(document).on("click", ".popup .image", function (){
        var url = $(this).attr("data-url");

        window.open(url);
    });

    $(document).on("click", ".topBtn", function (){
        $( 'html, body' ).animate( { scrollTop : 0 }, 400 );
    });

    $(document).on("click", ".writeBtn", function (){
        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = baseUrl + "login/local/";
               return;
           } else {
                return;
           }
       }

       var userType = $(this).attr("data-userType");

       if(userType == "NORMAL" || userType == "S-NORMAL") {
            window.location.href = "/profile/write/";
       } else if(userType == "COMPANY" || userType == "admin") {
            window.location.href = "/audi/write/";
       } else{
            alert("미승인 회원입니다. 문의하기를 통해 문의해 주세요.");
            return;
       }
    });


    $(document).on("click", ".castReviewBox", function (){
       var num = $(this).attr("data-num");

       if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = baseUrl + "login/local/";
               return;
           } else {
                return;
           }
       }

       window.location.href = "/lounge/notice/viewer/"+num+"/";
    });
});

function updateCount(num){
    $.ajax({
      url: "/common/updateBannerCount/",
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
      url: "/common/updateCounting/",
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
      url: "/common/updatePick/",
      type: "GET",
      dataType: "json",
      data:{"userID":userID, "tableName" : tableName, "nowType" : nowType, "num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });
}