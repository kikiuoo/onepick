$(document).ready(function(){
    $(document).on("click", ".sendBtn2", function(){

        var title = $("#title").val();
        var content = $("#content").val();


        if( title == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        if( content == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        $("#saveQanda").submit();
    });


    // 기본정보 선택시 글자 색상 변경
    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });

});
