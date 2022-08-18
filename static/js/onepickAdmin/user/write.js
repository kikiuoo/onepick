$(document).ready(function(){

    var now = new Date();
    var year = now.getFullYear();
    var mon = (now.getMonth() + 1) > 9 ? ''+(now.getMonth() + 1) : '0'+(now.getMonth() + 1);
    var day = (now.getDate()) > 9 ? ''+(now.getDate()) : '0'+(now.getDate());
    //년도 selectbox만들기
    for(var i = 1960 ; i <= year ; i++) {
        if( brith1 == i ){
            $('#brith1').append('<option value="' + i + '" selected>' + i + '년</option>');
        }else{
             $('#brith1').append('<option value="' + i + '">' + i + '년</option>');
        }
    }

    // 월별 selectbox 만들기
    for(var i=1; i <= 12; i++) {
        var mm = i > 9 ? i : "0"+i ;

        if( brith2 == mm ) {
            $('#brith2').append('<option value="' + mm + '" selected>' + mm + '월</option>');
        }else{
            $('#brith2').append('<option value="' + mm + '">' + mm + '월</option>');
        }
    }

    // 일별 selectbox 만들기
    for(var i=1; i <= 31; i++) {
        var dd = i > 9 ? i : "0"+i ;
        if( brith3 == dd ) {
             $('#brith3').append('<option value="' + dd + '" selected>' + dd+ '일</option>');
        }else{
             $('#brith3').append('<option value="' + dd + '">' + dd+ '일</option>');
        }

    }

    $(document).on("click", ".sendBtn", function (){

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

            if( name == "" ){
                alert("이름을 입력해주세요.");
                return;
            }

            if( email1 == "" || email2 == "" ){
                alert("이메일을 정확히 입력해주세요.");
                return;
            }
            if (phone1 == "" || phone2 == "" || phone3 == "") {
                alert("전화번호를 정확히 입력해주세요.");
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
        }

        $("#saveUserForm").submit();
    });

    $(document).on("click", ".image", function (){
        var url = $(this).attr("data-url");

        window.open("https://myonepick.com"+url);
    });

    $(document).on("click", ".sendBtn2", function (){
        var num = $(this).attr("data-num");

        updateCompany(num);
    });
});

function updateCompany(num){
   $.ajax({
      url: "/onepickAdmin/user/updateComany/",
      type: "GET",
      dataType: "json",
      data:{"num" : num},

      success: function(data){
          if( data.code == "0" ){
              alert("승인이 완료되었습니다.");
              window.location.reload();
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}
