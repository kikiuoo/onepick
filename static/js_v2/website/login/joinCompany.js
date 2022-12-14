$(document).ready(function(){

     $(document).on("click", ".overlapCheck", function (){
        var userID = $("#userID").val();

        if( userID == "" ){
            alert("사용 할 아이디를 입력해주세요");
            return
        }

        checkOverlapID(userID);
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

    $(document).on("change", ".upload-hidden", function (){
        var thisImage = $(this);
        var id = $(this).attr("id");

        var imageTag = "";
        var imageFile = "";
        var imageDel = "";

        if( id == "input-logo" ){
            imageTag = $("#logo .addImage");
            imageFile = $("#logo .imageInfo");
            imageDel = $("#logo .delBtn");
        }else if( id == "input-license" ){
            imageTag = $("#licenseImage .addImage");
            imageFile = $("#licenseImage .imageInfo");
            imageDel = $("#licenseImage .delBtn");
        }else if( id == "input-artLicense" ){
            imageTag = $("#artLicense .addImage");
            imageFile = $("#artLicense .imageInfo");
            imageDel = $("#artLicense .delBtn");
        }

        if (!thisImage[0].files[0].type.match(/image\//)) return;//image 파일만

        imageTag.text('');
        imageFile.css("color", "#1f1f1f");
        imageFile.text(thisImage[0].files[0].name);
        imageDel.css("display", "inline-block");

        var reader = new FileReader();
        reader.onload = function(e){
            var src = e.target.result;
            imageTag.css("background-image", "url('"+src+"')");
            imageTag.css("background-size", "100% auto");
        }

        reader.readAsDataURL(thisImage[0].files[0]);
    });


    $(document).on("click", ".delBtn", function (e){
        e.preventDefault();
        e.stopPropagation();

        var id = $(this).attr("data-id");

        var imageTag = $(this).parent().children(".addImage");
        var imageFile = $(this).parent().children(".imageInfo");
        var imageDel = $(this).parent().children(".delBtn");

        imageTag.css("background-image", "url('/static/image/web_v2/gallery-add.png')");
        imageTag.css("background-size", "auto");
        imageFile.css("color", "#959595");
        imageDel.css("display", "none");

        if( id == "license" ){
            imageFile.text("사업자 등록증을 첨부하세요.");
        }else if ( id == "artLicense" ){
            imageFile.text("대중 문화 예술 기획업 등록증을 첨부하세요.");
        }else if ( id == "logo" ){
            imageFile.text("이미지를 첨부하세요.");
        }

        $("#input-"+id).val("");

    });



    $(document).on("click", ".sendBtn", function (){

        var userID = $("#userID").val();
        var overlap = $("#overlap").is(":checked");
        var pw1 = $("#pw1").val();
        var pw2 = $("#pw2").val();
        var name = $("#name").val();
        var email = $("#email").val();
        var phone = $("#phone").val();
        var confirmCheck = $("#confirmCheck").is(":checked");

        var companyName = $("#companyName").val();
        var license = $("#license").val();
        var companyAddr1 = $("#companyAddr1").val();
        var companyAddr2 = $("#companyAddr2").val();
        var webSite = $("#webSite").val();
        var logo = $("#input-logo").val();
        var licenseImage = $("#input-license").val();

        if( overlap == false ){
            alert("아이디 중복체크를 해주세요.");
            return;
        }

        if( pw1 == "" || pw2 == "" ){
            alert("비밀번호를 입력해주세요.");
            return;
        }

        if( pw1 != pw2 ){
            alert("입력하신 비밀번호가 다릅니다.");
            return;
        }

        if( name == "" ){
            alert("담당자 이름을 입력해주세요.");
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

        /*  2022-08-10 대표님 요청으로 필수항목 제외.
        if( artLicense == "" ){
            alert("대중 문화 예술 기획업 등록증 이미지를 등록해주세요.");
            return;
        }
        */

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

function checkOverlapID(userID){

   $.ajax({
      url: "/login/ajax/checkOverlapID/",
      type: "GET",
      dataType: "json",
      data:{"userID" : userID},

      success: function(data){
          if( data.code == "0" ){
              alert("사용가능한 아이디입니다.");
              $("#overlap").attr("checked","true");
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}

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