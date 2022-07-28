$(document).ready(function() {

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

    $("#userPW").on("keyup",function(key){
        if(key.keyCode==13){
            $(".loginBtn").trigger("click");
        }
    });

});


function login(username, password){
   $.ajax({
      url: "/onepickAdmin/loginCheck/",
      type: "GET",
      dataType: "json",
      data:{"username" : username, "password" : password},

      success: function(data){
          if( data.code == "0" ){
              window.location.href = "/onepickAdmin/";
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}
