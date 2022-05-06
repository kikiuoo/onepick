$(document).ready(function(){

    $(document).on("click", ".sendBtn", function(){
        var logoImage = $("#logo").val();
        var regImage = $("#regImage").val();
        var companyName = $("#companyName").val();
        var registration = $("#registration").val();
        var name = $("#name").val();
        var phone2 = $("#phone2").val();
        var phone3 = $("#phone3").val();

        var addr1 = $("#sample4_roadAddress").val();
        var addr2 = $("#sample4_detailAddress").val();

        if( logoImage == "" ){
            alert("로고 이미지를 추가해주세요.");
            return;
        }

        if( regImage == "" ){
            alert("사업자등록증 이미지를 추가해주세요.");
            return;
        }

        if( companyName == "" ){
            alert("회사명을 입력해주세요.");
            return;
        }

        if( registration == "" ){
            alert("사업자등록번호를 입력해주세요.");
            return;
        }
        
        if( addr1 == "" || addr2 == "" ){
            alert("사업장 주소를 입력해주세요.");
            return;
        }

        if( name == "" ){
            alert("담당자명을 입력해주세요.");
            return;
        }

        if( phone2 == "" || phone3 == ""){
            alert("담당자 연락처를 입력해주세요.");
            return;
        }

        $("#saveCompany").submit();
    });

});



// 다음지도 API
function sample4_execDaumPostcode() {
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
            //document.getElementById('sample4_postcode').value = data.zonecode;
            document.getElementById("sample4_roadAddress").value = roadAddr;
            //document.getElementById("sample4_jibunAddress").value = data.jibunAddress;

        }
    }).open();
}