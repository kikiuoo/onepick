$(document).ready(function(){

    $(document).on("click", ".idFindBtn", function (){
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
           $(".idFindBtn").trigger("click");
       }
    });

    $(document).on("click", ".s_userID", function(){

        var values = $(".s_userID:checked").val();

        $("#userID").val(values);
    });

    $(document).on("click", ".pwFindBtn", function(){
        var userID = $("#userID").val();
        var userName = $("#userName2").val();

        if( userID == "" ){
            alert("아이디를 입력해주세요");
            return;
        }

        if( userName == "" ){
            alert("이름을 입력해주세요");
            return;
        }

        chechUser_pw( userID, userName );
    });

     $(document).on("click", ".setPWBtn", function(){
        var userID = $("#userID").val();
        var pw1 = $("#pw1").val();
        var pw2 = $("#pw2").val();

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

function chechUser_pw( userID, userName ){
   $.ajax({
      url: "/users/findPW/",
      type: "POST",
      dataType: "json",
      data:{"userID" : userID, "userName" : userName},

      success: function(data){
          if( data.code == "0" ){
              $(".findPw").css("display", "block");
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
      url: "/users/updatePW/",
      type: "POST",
      dataType: "json",
      data:{"userID" : userID, "password" : password},

      success: function(data){
          if( data.code == "0" ){
             alert("비밀번호가 변경되었습니다.");
             window.location.href = "/users/login/local/";
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}
