$(document).ready(function() {

    $(document).on("click", ".sendBtn", function (){
        let chk_Val = [];

       $('input:checkbox[name=paramRadio]').each(function (index) {
            if($(this).is(":checked")==true){
                chk_Val.push($(this).val());
            }
        });

        var saveChk = chk_Val.join(',');
        var profileNum = $("#profileNum").val();

        if( saveChk == "" ){
            alert("회원의 이미지를 선택해주세요.");
            return;
        }

        saveClassfy(saveChk, profileNum)
    });

});

function saveClassfy(saveChk, profileNum) {
    $.ajax({
        url: "/onepickAdmin/classfy/saveClassfy/",
        type: "GET",
        dataType: "json",
        data: {"saveChk": saveChk , "profileNum" : profileNum},
        success: function (data) {
            window.location.reload();
        },
        error: function (request, status, error) {
            alert(error);
        }
    });
}
