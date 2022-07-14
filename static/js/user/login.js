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

        if( type == "oldUser" || type == "" || type == "" ){
            // 기존 회원 정보 연동.
            window.location.href = "/users/join/"+id+"/oldUser/"
        }else{
            // 소셜로그인 연동
            // 로컬 스토리지에 저장 후 입력폼으로 이동 후 소셜 로그인과 체크 후 제어.
            window.localStorage.setItem("userID", id);
            window.location.href = "/users/joinView/";
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

    $(document).on("click", ".reInputBtn", function (){
        $("#userName").val('');
        $("#userPhone").val('');

        $(".userInfoBox").css("display", "block");
        $(".loginBox2").css("display", "none");
        $(".loginBox3").css("display", "none");
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
            $(".loginBox3").css("display", "none");

            alert("검색된 데이터가 없습니다.");
        }else{
            $(".userInfoBox").css("display", "none");
            $(".loginBox3").css("display", "none");
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
      type: "GET",
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
