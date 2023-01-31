$(document).ready(function(){

    $(document).on("click", ".idFindBtn", function (){
        var userName = $("#userName").val();
        var confirmCheck = $("#confirmCheck").is(":checked");
        var phone = $("#phone").val();

        if( userName == "" ){
            alert("이름을 입력해주세요");
            return;
        }

        if( confirmCheck == false ){
            alert("전화번호를 인증해주세요.");
            return;
        }

        find_old_user(userName, phone);
    });

     $(document).on("click", ".confirmPhone", function(){
        var phone = $("#phone").val();

        if( phone == "" ){
            alert("전화번호를 입력해주세요.");
            return;
        }

        idFindConfirm( phone );
    });


     $(document).on("click", ".findConfirm", function(){
        var phone = $("#phone").val();
        var confirm = $("#confirm").val();

        if( phone == "" ){
            alert("전화번호를 입력해주세요");
            return
        }

        if( confirm == "" ){
            alert("인증번호를 입력해주세요");
            return
        }

        var check = $(".findConfirm").attr("data-check");

        if( check == "true" ){
            return;
        }

        checkConfirm(phone, confirm)
    });


     $(document).on("click", ".loginBtn", function (){
        window.location.href = "/login/local/";
     });






     $(document).on("click", ".confirmPhone_pw", function(){
        var phone = $("#phone_pw").val();

        if( phone == "" ){
            alert("전화번호를 입력해주세요.");
            return;
        }

        pwFindConfirm( phone );
    });


     $(document).on("click", ".findConfirm_pw", function(){
        var phone = $("#phone_pw").val();
        var confirm = $("#confirm_pw").val();

        if( phone == "" ){
            alert("전화번호를 입력해주세요");
            return
        }

        if( confirm == "" ){
            alert("인증번호를 입력해주세요");
            return
        }

        var check = $(".findConfirm").attr("data-check");

        if( check == "true" ){
            return;
        }

        checkConfirm_pw(phone, confirm)
    });

    $(document).on("click", ".pwFindBtn", function (){
        var userName = $("#userID_pw").val();
        var confirmCheck = $("#confirmCheck_pw").is(":checked");
        var phone = $("#phone_pw").val();

        if( userName == "" ){
            alert("이름을 입력해주세요");
            return;
        }

        if( confirmCheck == false ){
            alert("전화번호를 인증해주세요.");
            return;
        }

        chechUser_pw(userName, phone);
    });

     $(document).on("click", ".savePWBtn", function(){
        var userID = $("#userID_pw").val();
        var pw1 = $("#pw1").val();
        var pw2 = $("#pw2").val();

        if( userID == "" ){
            alert("아이디를 입력해주세요.");
            return;
        }

        if( pw1 == "" || pw2 == "" ){
            alert("비밀번호를 입력해주세요.");
            return;
        }

        if( pw1 != pw2 ){
            alert("비밀번호를 정확히 입력해주세요.");
            return;
        }

         update_pw( userID, pw1 );
    });







     $(document).on("click", ".checkVerifi", function(){
        var userID = $("#userID").val();
        var phone = $("#phone").val();
        var verification = $("#verification").val();

        if( phone == "" ){
            alert("전화번호를 입력해주세요.");
            return;
        }

        if( verification == "" ){
            alert("인증번호를 입력해주세요.");
            return;
        }

        checkConfirm( phone, verification );
    });
});


function idFindConfirm(phoneNum){

   $.ajax({
      url:  baseUrl +"login/ajax/idFindPhoneComfirm/",
      type: "GET",
      dataType: "json",
      data:{"phoneNum" : phoneNum},

      success: function(data){
          if( data.code == "0" ){
              alert("인증번호가 전송되었습니다.");
              $(".confirmPhone").text("인증 번호 재전송");
              $(".confirmPhone").css("border", "0px");
              $(".findConfirm").removeClass("disabled");
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}

function checkConfirm(phoneNum, confirm){
   $.ajax({
      url: baseUrl +"login/ajax/checkConfirm/",
      type: "GET",
      dataType: "json",
      data:{"phoneNum" : phoneNum, "confirm" : confirm},

      success: function(data){
          if( data.code == "0" ){
              alert("인증이 완료되었습니다.");
              $("#confirmCheck").attr("checked","true");
              $(".findConfirm").attr("data-check","true");
              $(".confirmPhone").attr("data-check","true");

              $(".findConfirm").addClass("disabled");
              $(".findConfirm").css("background-color","#d7d7d7");
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}

function find_old_user(userName, userPhone){
    $.ajax({
      url: baseUrl +"login/ajax/findUser/",
      type: "GET",
      dataType: "json",
      data:{"userName":userName, "userPhone" : userPhone},

      success: function(data){
          if( data.code == "1" ){
              alert(data.message);
          }else{
              alert(data.userType);
              if ( data.userType == "oldUser" || data.userType == "OLDUSER" ){
                  $(".uID").text(data.userID);
                  $(".loginBox").css("display", "none");
                  $(".userInfo").css("display", "block");
              }else{
                  alert("SNS로 로그인하셨습니다.\n\r메인화면 오른쪽 하단 [문의하기로] 문의해주세요.");
              }
          }
      },
      error: function (request, status, error){

      }
   });
}


function pwFindConfirm(phoneNum){

   $.ajax({
      url:  baseUrl +"login/ajax/idFindPhoneComfirm/",
      type: "GET",
      dataType: "json",
      data:{"phoneNum" : phoneNum},

      success: function(data){
          if( data.code == "0" ){
              alert("인증번호가 전송되었습니다.");
              $(".confirmPhone_pw").text("인증 번호 재전송");
              $(".confirmPhone_pw").css("border", "0px");
              $(".findConfirm_pw").removeClass("disabled");
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}

function checkConfirm_pw(phoneNum, confirm){
   $.ajax({
      url: baseUrl +"login/ajax/checkConfirm/",
      type: "GET",
      dataType: "json",
      data:{"phoneNum" : phoneNum, "confirm" : confirm},

      success: function(data){
          if( data.code == "0" ){
              alert("인증이 완료되었습니다.");
              $("#confirmCheck_pw").attr("checked","true");
              $(".findConfirm_pw").attr("data-check","true");
              $(".confirmPhone_pw").attr("data-check","true");

              $(".findConfirm_pw").addClass("disabled");
              $(".findConfirm_pw").css("background-color","#d7d7d7");
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}

function chechUser_pw( userID, userPhone ){
   $.ajax({
      url: baseUrl +"login/findPW/",
      type: "POST",
      dataType: "json",
      data:{"userID" : userID, "userPhone" : userPhone},

      success: function(data){
          if( data.code == "0" ){
              $(".pwFindBox").css("display", "none");
              $(".resetPWBox").css("display", "block");
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}


function update_pw( userID, password ){
   $.ajax({
      url: baseUrl +"login/updatePW_local/",
      type: "GET",
      dataType: "json",
      data:{"userID" : userID, "password" : password},

      success: function(data){
          if( data.code == "0" ){
             alert("비밀번호가 변경되었습니다.");
             window.location.href = baseUrl +"login/local/";
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}
