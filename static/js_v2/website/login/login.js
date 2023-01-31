$(document).ready(function(){

    $(document).on("click", ".socialBox .socialBtn", function (){
        var loginType = $(this).attr("id");
        var reUrl = $("#reUrl").val();

        window.localStorage.setItem("reUrl", reUrl);

        // 각 API 구현 필요.
        if( loginType == "kakaoLogin" ){
            window.location.href = baseUrl +"login/kakao/";
        }else if( loginType == "gogleLogin" ){
            window.location.href = baseUrl +"login/google/";
        }else if( loginType == "appleLogin" ){
           // window.location.href = baseUrl +"login/apple/";
        }else if( loginType == "naverLogin" ){
            window.location.href = baseUrl +"login/naver/";
        }
    });

    // 기존 회원 로그인
    $(document).on("click", ".loginBtn", function (){
        var userID = $("#userID").val();
        var userPW = $("#userPW").val();
        var reUrl = $("#reUrl").val();

        if( userID == "" ){
            alert("아이디를 입력해 주세요.");
            return;
        }
        else if( userPW == "" ){
            alert("패스워드를 입력해 주세요.");
            return;
        }
        login(userID, userPW, reUrl);
    });

    $("#userPW").on("keyup",function(key){
        if(key.keyCode==13){
            $(".loginBtn").trigger("click");
        }
    });

    $(document).on("click", ".searchInfo", function (){
        window.location.href = baseUrl +"login/findUser/"
    });


    $(document).on("click", ".joinInfo span", function (){
        window.location.href = baseUrl +"login/joinView/";
    });

    $(document).on("click", ".reInputBtn", function (){
        $("#userName").val('');
        $("#userPhone").val('');

        $(".userInfoBox").css("display", "block");
        $(".loginBox2").css("display", "none");
        $(".loginBox3").css("display", "none");
    });

});


function login(username, password, reUrl){
   $.ajax({
      url: baseUrl +"login/logincallback/",
      type: "GET",
      dataType: "json",
      data:{"username" : username, "password" : password},

      success: function(data){
          if( data.code == "0" ){
              if( reUrl != "" ){
                  window.location.href = reUrl;
              }else {
                  window.location.href = baseUrl;
              }
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}
