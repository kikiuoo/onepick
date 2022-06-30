$(document).ready(function(){

    var now = new Date();
    var year = now.getFullYear();
    var mon = (now.getMonth() + 1) > 9 ? ''+(now.getMonth() + 1) : '0'+(now.getMonth() + 1);
    var day = (now.getDate()) > 9 ? ''+(now.getDate()) : '0'+(now.getDate());
    //년도 selectbox만들기
    for(var i = 1960 ; i <= year ; i++) {
        $('#brith1').append('<option value="' + i + '">' + i + '</option>');
    }

    // 월별 selectbox 만들기
    for(var i=1; i <= 12; i++) {
        var mm = i > 9 ? i : "0"+i ;
        $('#brith2').append('<option value="' + mm + '">' + mm + '</option>');
    }

    // 일별 selectbox 만들기
    for(var i=1; i <= 31; i++) {
        var dd = i > 9 ? i : "0"+i ;
        $('#brith3').append('<option value="' + dd + '">' + dd+ '</option>');
    }


    if(joinType == "social" && localStorage.getItem('userID') != "" ){
        $("#oldUserID").val( localStorage.getItem('userID') );
        window.localStorage.removeItem('userID');
    }

    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });

    $(document).on("click", ".userType", function (){
        var userType = $(".userType:checked").val();

        if( userType == "S-COMPANY"){
            $(".companyInfo").css("display", "block");
            $(".nonCompany").css("display", "none");
            $(".cPhone").text("담당자 연락처");
            $(".cName").text("담당자 이름");
        }else{
            $(".companyInfo").css("display", "none");
            $(".nonCompany").css("display", "block");
            $(".cPhone").text("전화번호");
            $(".cName").text("이름");
        }
    });

    $(document).on("change", "#email_select", function (){
        var data = $("#email_select").find("option:selected").val();
        $("#email2").val(data);
    });

    $(document).on("click", ".confirmPhone", function (){
        var phone1 = $("#phone1").find("option:selected").val();
        var phone2 = $("#phone2").val();
        var phone3 = $("#phone3").val();

        if( phone1 == "" || phone2 == "" || phone3 == "" ){
            alert("전화번호를 입력해주세요");
            return
        }

        var check = $(".confirmPhone").attr("data-check");

        if( check == "true" ){
            return;
        }

        saveConfirm(phone1+phone2+phone3);
    });

    $(document).on("click", ".findConfirm", function(){
        var phone1 = $("#phone1").find("option:selected").val();
        var phone2 = $("#phone2").val();
        var phone3 = $("#phone3").val();
        var confirm = $("#confirm").val();
        
        if( phone1 == "" || phone2 == "" || phone3 == "" ){
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

        checkConfirm(phone1+phone2+phone3, confirm)
    });

    $(document).on("click", ".findAddr, .findAddr2", function (){
        var type = $(this).attr("data-type");

        sample4_execDaumPostcode(type);
    });

    $(document).on("change", ".upload-hidden", function (){
        var thisImage = $(this);
        var id = $(this).attr("id");

        var imageTag = "";
        var imageAdd = "";

        if( id == "input-logo" ){
            imageTag = $("#logo");
            imageAdd = $("#logo .addImage");
        }else if( id == "input-license" ){
            imageTag = $("#licenseImage");
            imageAdd = $("#license .addImage");
        }else if( id == "input-artLicense" ){
            imageTag = $("#artLicense");
            imageAdd = $("#artLicense .addImage");
        }

        if (!thisImage[0].files[0].type.match(/image\//)) return;//image 파일만

        imageAdd.css("display", "none");
        imageTag.text('');

        var reader = new FileReader();
        reader.onload = function(e){
            var src = e.target.result;
            imageTag.css("background-image", "url('"+src+"'");
        }

        reader.readAsDataURL(thisImage[0].files[0]);
    });

    $(document).on("click", ".sendBtn", function (){

        var userType = $(".userType:checked").val();
        var pw1 = $("#pw1").val();
        var pw2 = $("#pw2").val();
        var name = $("#name").val();
        var email1 = $("#email1").val();
        var email2 = $("#email2").val();
        var phone1 = $("#phone1").val();
        var phone2 = $("#phone2").val();
        var phone3 = $("#phone3").val();
        var confirmCheck = $("#confirmCheck").is(":checked");
        var brith1 = $("#brith1").find("option:selected").val();
        var brith2 = $("#brith2").find("option:selected").val();
        var brith3 = $("#brith3").find("option:selected").val();
        var gender = $("#gender").val();
        var addr1 = $("#addr1").val();
        var addr2 = $("#addr2").val();

        var companyName = $("#companyName").val();
        var license = $("#license").val();
        var companyAddr1 = $("#companyAddr1").val();
        var companyAddr2 = $("#companyAddr2").val();
        var webSite = $("#webSite").val();
        var logo = $("#input-logo").val();
        var licenseImage = $("#input-license").val();
        var artLicense = $("#input-artLicense").val();

        if( userType == "NORMAL"){

            if( joinType == "oldUser"){
                if( pw1 == "" || pw2 == "" ){
                    alert("비밀번호를 입력해주세요.");
                    return;
                }

                if( pw1 != pw2 ){
                    alert("입력하신 비밀번호가 다릅니다.");
                    return;
                }
            }

            if( name == "" ){
                alert("이름을 입력해주세요.");
                return;
            }

            if( email1 == "" || email2 == "" ){
                alert("이메일을 정확히 입력해주세요.");
                return;
            }

            if( phone1 == "" || phone2 == "" || phone3 == "" ){
                alert("전화번호를 정확히 입력해주세요.");
                return;
            }

            if( confirmCheck == false){
                alert("전화번호를 인증해주세요.");
                return;
            }

            if( brith1 == "" || brith2 == "" || brith3 == "" ){
                alert("생년월일을 정확히 입력해주세요.");
                return;
            }

            if( addr1 == "" || addr2 == "" ){
                alert("주소를 정확히 입력해주세요.");
                return;
            }
        }else{
            if( joinType == "oldUser"){
                if( pw1 == "" || pw2 == "" ){
                    alert("비밀번호를 입력해주세요.");
                    return;
                }

                if( pw1 != pw2 ){
                    alert("입력하신 비밀번호가 다릅니다.");
                    return;
                }
            }

            if( name == "" ){
                alert("담당자 이름을 입력해주세요.");
                return;
            }

            if( email1 == "" || email2 == "" ){
                alert("이메일을 정확히 입력해주세요.");
                return;
            }

            if( phone1 == "" || phone2 == "" || phone3 == "" ){
                alert("담당자 연락처를 정확히 입력해주세요.");
                return;
            }

            if( confirmCheck == false){
                alert("담당자 연락처를 인증해주세요.");
                return;
            }
            
            if( companyName == "" ){
                alert("사업자명을 입력해주세요.");
                return;
            }
            
            if( license == "" ){
                alert("사업자 등록번호를 입력해주세요.");
                return;
            }
            
            if( companyAddr1 == "" || companyAddr2 == "" ){
                alert("사업장 주소를 입력해주세요.");
                return;
            }

            if( webSite == "" ){
                alert("웹사이트를 입력해주세요.");
                return;
            }

            if( logo == "" ){
                alert("로고 이미지를 등록해주세요.");
                return;
            }

            if( licenseImage == "" ){
                alert("사업자 등록증 이미지를 등록해주세요.");
                return;
            }

            if( artLicense == "" ){
                alert("대중 문화 예술 기획업 등록증 이미지를 등록해주세요.");
                return;
            }
        }

        $("#saveUserForm").submit();
    });

    $(document).on("change", ".emailCheck, .phoneCheck", function(){

        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_on.png")');
        }else{
            $(this).css("color", "#c0c0c0");
            $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_off.png")');
        }
    });

});


function saveConfirm(phoneNum){
   $.ajax({
      url: "/users/ajax/phoneComfirm/",
      type: "POST",
      dataType: "json",
      data:{"phoneNum" : phoneNum, "csrfmiddlewaretoken" : csrftoken},

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
      type: "POST",
      dataType: "json",
      data:{"phoneNum" : phoneNum, "confirm" : confirm, "csrfmiddlewaretoken" : csrftoken},

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