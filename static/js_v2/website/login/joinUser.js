$(document).ready(function(){

    $('[data-toggle="datepicker"]').datepicker({
        format: 'yyyy-mm-dd'
    }).on( "change", function() {
        $(this).css("color", "#1f1f1f");
        $(this).css("border", "1px solid #1f1f1f")
        $(this).css("background-color", "#fff");
    });


    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
        $(this).css("border", "1px solid #1f1f1f")
        $(this).css("background-color", "#fff");
    });


    $(document).on("click", ".confirmPhone", function (){
        var phone = $("#phone").val();

        if( phone == "" ){
            alert("전화번호를 입력해주세요");
            return
        }

        var check = $(".confirmPhone").attr("data-check");

        if( check == "true" ){
            return;
        }

        saveConfirm(phone);
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

    $(document).on("click", ".findAddr2", function (){
        var type = $(this).attr("data-type");

        sample4_execDaumPostcode(type);
    });



    $(document).on("click", ".sendBtn", function (){

        var name = $("#name").val();
        var email = $("#email").val();
        var phone = $("#phone").val();
        var confirmCheck = $("#confirmCheck").is(":checked");

        var birth = $("#birth").val();
        var gender = $("#gender").find("option:selected").val();
        var companyAddr1 = $("#companyAddr1").val();
        var companyAddr2 = $("#companyAddr2").val();


        if( name == "" ){
            alert("이름을 입력해주세요.");
            return;
        }

        if( email == "" ){
            alert("이메일을 정확히 입력해주세요.");
            return;
        }

        var regExp = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;

        if (email.match(regExp) == null) {
            alert("이메일형식을 확인해주세요.");
            return;
        }

        if( phone == "" ){
            alert("연락처를 정확히 입력해주세요.");
            return;
        }

        if( confirmCheck == false){
            alert("연락처를 인증해주세요.");
            return;
        }

        if( birth == "" ){
            alert("생년월일을 입력해주세요.");
            return;
        }

        if( gender == "" ){
            alert("성별을 선택해주세요.");
            return;
        }

        if( companyAddr1 == "" || companyAddr2 == "" ){
            alert("주소를 입력해주세요.");
            return;
        }

        $("#saveUserForm").submit();
    });

    $(document).on("change", ".emailCheck, .phoneCheck", function(){

        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("/static/image/web_v2/tick-square_on.png")');
            $(this).children("input").attr("checked","true");;
        }else{
            $(this).css("color", "#c0c0c0");
            $(this).children("div").css("background-image", 'url("/static/image/web_v2/tick-square_off.png")');
            $(this).children("input").removeAttr("checked");;
        }
    });

});


function saveConfirm(phoneNum){

   $.ajax({
      url: "/login/ajax/phoneComfirm/",
      type: "GET",
      dataType: "json",
      data:{"phoneNum" : phoneNum},

      success: function(data){
          if( data.code == "0" ){
              alert("인증번호가 전송되었습니다.");
              $(".confirmPhone").text("인증 번호 재전송");
              $(".confirmPhone").css("border","0px");
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
      url: "/login/ajax/checkConfirm/",
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


 function sample4_execDaumPostcode(type) {
    new daum.Postcode({
        oncomplete: function(data) {
            // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

            // 도로명 주소의 노출 규칙에 따라 주소를 표시한다.
            // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
            var roadAddr = data.roadAddress; // 도로명 주소 변수
            var extraRoadAddr = ''; // 참고 항목 변수

            // 법정동명이 있을 경우 추가한다. (법정리는 제외)
            // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
            if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
                extraRoadAddr += data.bname;
            }
            // 건물명이 있고, 공동주택일 경우 추가한다.
            if(data.buildingName !== '' && data.apartment === 'Y'){
               extraRoadAddr += (extraRoadAddr !== '' ? ', ' + data.buildingName : data.buildingName);
            }
            // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
            if(extraRoadAddr !== ''){
                extraRoadAddr = ' (' + extraRoadAddr + ')';
            }

            // 우편번호와 주소 정보를 해당 필드에 넣는다.

            if( type == "company" ){
                $("#companyAddr1").val("("+data.zonecode+")" +roadAddr );
                $("#companyAddr1").css("background-color" , "#fff");
                $("#companyAddr1").css("border" , "1px solid #1f1f1f");
            }else{
                $("#addr1").val("("+data.zonecode+")" +roadAddr );
            }
        }
    }).open();
}