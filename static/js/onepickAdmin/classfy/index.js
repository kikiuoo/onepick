$(document).ready(function() {

    $(document).on("click", ".sendBtn", function (){
        let chk_Val = [];
        let chk_Val2 = [];
        let chk_Val3 = [];
        let chk_Val4 = [];

       $('input:checkbox[name=faceRadio]').each(function (index) {
            if($(this).is(":checked")==true){
                chk_Val.push($(this).val());
            }
        });


       $('input:checkbox[name=bodyRadio]').each(function (index) {
            if($(this).is(":checked")==true){
                chk_Val2.push($(this).val());
            }
        });


       $('input:checkbox[name=imgRadio]').each(function (index) {
            if($(this).is(":checked")==true){
                chk_Val3.push($(this).val());
            }
        });


       $('input:checkbox[name=jobRadio]').each(function (index) {
            if($(this).is(":checked")==true){
                chk_Val4.push($(this).val());
            }
        });

        var saveChk_face = chk_Val.join(',');
        var saveChk_body = chk_Val2.join(',');
        var saveChk_img = chk_Val3.join(',');
        var saveChk_job = chk_Val4.join(',');
        var profileNum = $("#profileNum").val();

        if( saveChk_face == "" ){
            alert("회원의 얼굴형을 선택해주세요.");
            return;
        }
        
        if( saveChk_body == "" ){
            alert("회원의 체형을 선택해주세요.");
            return;
        }       
        
        if( saveChk_img == "" ){
            alert("회원의 이미지를 선택해주세요.");
            return;
        }        
        
        if( saveChk_job == "" ){
            alert("회원의 직업을 선택해주세요.");
            return;
        }

        saveClassfy(saveChk_face, saveChk_body, saveChk_img, saveChk_job, profileNum)
    });


    $(document).on("click", ".instagram, .youtube", function (){
        var b_rul = $(this).attr("data-url");

        var Url = /(http|https):\/\/((\w+)[.])+(asia|biz|cc|cn|com|de|eu|in|info|jobs|jp|kr|mobi|mx|name|net|nz|org|travel|tv|tw|uk|us)(\/(\w*))*$/i;
        var urlTest = Url.test(b_rul);

        var Url2 = /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
        var urlTest2 = Url2.test(b_rul);

        if(!urlTest && !urlTest2){
            alert("올바른 url이 아닙니다.");
            return false;
        }

        window.open(b_rul);
    });


    $(document).on("click", ".resetBox", function (){
       window.location.reload();
    });
});

function saveClassfy(saveChk_face, saveChk_body, saveChk_img, saveChk_job,  profileNum) {
    $.ajax({
        url: "/onepickAdmin/classfy/saveClassfy/",
        type: "GET",
        dataType: "json",
        data: {"saveChk_face": saveChk_face ,"saveChk_body": saveChk_body
               ,"saveChk_img": saveChk_img ,"saveChk_job": saveChk_job , "profileNum" : profileNum},
        success: function (data) {
            window.location.reload();
        },
        error: function (request, status, error) {
            alert(error);
        }
    });
}
