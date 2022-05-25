$(document).ready(function(){

    $(document).on("click", ".findUser", function (){
        var userName = $("#userName").val();
        var userPhone = $("#userPhone").val();

        if( userName == "" ){
            alert("이름을 입력해주세요");
            return;
        }
        
        if( userPhone == "" ){
            alert("전화번호를 입력해주세요");
            return;
        }

        find_old_user(userName, userPhone);
    });

    $(document).on("click", ".findBtn", function (){

        var id =  $('.s_userID:checked').val();
        var type =  $('.s_userID:checked').attr("data-type");

        alert(id + " " + type);

        if( type == "" ){
            // 기존 회원 정보 연동.
        }else{
            // 소셜로그인 연동
        }

    });


    $(document).on("click", ".socialBox .socialBtn", function (){
        var loginType = $(this).attr("id");

        // 각 API 구현 필요.
        if( loginType == "kakaoLogin" ){
            window.location.href = "/users/login/kakao/";
        }else if( loginType == "gogleLogin" ){
            window.location.href = "/users/login/google/";
        }else if( loginType == "appleLogin" ){
           // window.location.href = "/users/login/apple/";
        }else if( loginType == "naverLogin" ){
            window.location.href = "/users/login/naver/";
        }

    });

    $(document).on("keyup", "#userID, #userPW", function(e){
       if( e.keyCode == 13 ){
           $(".loginBtn").trigger("click");
       }
    });

    $(document).on("keyup", "#userName, #userPhone", function(e){
       if( e.keyCode == 13 ){
           $(".findUser").trigger("click");
       }
    });

    document.addEventListener('AppleIDSignInOnSuccess', (data) => {
         //handle successful response
         alert("AppleIDSignInOnSuccess")
         //todo success logic
    });
    //애플로 로그인 실패 시.
    document.addEventListener('AppleIDSignInOnFailure', (error) => {
         //handle error.
         alert("AppleIDSignInOnFailure")
         //todo fail logic
    });

});

function find_old_user(userName, userPhone){
    $.ajax({
      url: "/users/ajax/findOldUser/",
      type: "GET",
      dataType: "html",
      data:{"userName":userName, "userPhone" : userPhone},

      success: function(data){
        if( data == "" ){
            $(".userInfoBox").css("display", "block");
            $(".loginBox2").css("display", "none");
            $(".nonInfo").css("display", "block");
        }else{
            $(".userInfoBox").css("display", "none");
            $(".nonInfo").css("display", "none");

            $(".inputBox2").empty().append(data);
            $(".loginBox2").css("display", "block");
        }
      },
      error: function (request, status, error){

      }
   });
}
