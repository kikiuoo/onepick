$(document).ready(function(){

    $(document).on("change", ".textCheck", function(){

        var checked = $(this).children().is(":checked");

        if (checked == true) {
            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_on.png")');
            $(this).children("input").attr("checked", "true");
        }else{

            $(this).css("color", "#c0c0c0");
            $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_off.png")');
            $(this).children("input").removeAttr("checked", "true");
        }
    });


    $(document).on("click", ".sendBtn", function (){

        var quitCause = $(".quitCause:checked").val();
        var quitEtcCause = $("#quitEtcCause").val();
        var notView = $("#notView").is(":checked");

        if( quitCause == "etc" && quitEtcCause == ""){
            alert("탈퇴 사유를 입력해주세요.");
            return;
        }

        if( notView == false){
            alert("탈퇴 동의를 확인해주세요.");
            return;
        }

        $("#saveUserForm").submit();
    });

});


function saveConfirm(phoneNum){
   $.ajax({
      url: "/users/ajax/phoneComfirm/",
      type: "GET",
      dataType: "json",
      data:{"phoneNum" : phoneNum},

      success: function(data){
          if( data.code == "0" ){
              alert("인증번호가 전송되었습니다.");
              $(".confirmPhone").text("재전송");
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
      url: "/users/ajax/checkConfirm/",
      type: "GET",
      dataType: "json",
      data:{"phoneNum" : phoneNum, "confirm" : confirm},

      success: function(data){
          if( data.code == "0" ){
              alert("인증이 완료되었습니다.");
              $("#confirmCheck").attr("checked","true");
              $(".findConfirm").attr("data-check","true");
              $(".confirmPhone").attr("data-check","true");

              $(".findConfirm").css("background-color","#c0c0c0");
              $(".confirmPhone").css("background-color","#c0c0c0");
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
            }else{
                $("#addr1").val("("+data.zonecode+")" +roadAddr );
            }
        }
    }).open();
}