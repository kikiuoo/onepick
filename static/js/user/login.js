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

    $(document).on("keyup", "#userName, #userPhone", function(e){
       if( e.keyCode == 13 ){
           $(".findBtn").trigger("click");
       }
    });

    $(document).on("click", ".findBtn", function (){

        var id =  $('.s_userID:checked').val();
        var type =  $('.s_userID:checked').attr("data-type");

        if( type == "" ){
            // 기존 회원 정보 연동.
            window.location.href = "/users/join/"+id+"/oldUser/"
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

    // 기존 회원 로그인
    $(document).on("click", ".loginBtn", function (){
        var userID = $("#userID").val();
        var userPW = $("#userPW").val();

        if( userID == "" ){
            alert("아이디를 입력해 주세요.");
            return;
        }
        else if( userPW == "" ){
            alert("패스워드를 입력해 주세요.");
            return;
        }
        login(userID, userPW);
    });

    $(document).on("click", ".searchInfo", function (){
        window.location.href = "/users/findUser/"
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

function login(username, password){
   $.ajax({
      url: "/users/login/logincallback/",
      type: "POST",
      dataType: "json",
      data:{"username" : username, "password" : password},

      success: function(data){
          if( data.code == "0" ){
              window.location.href = "/";
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}
