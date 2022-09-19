$(document).ready(function(){


    // 기본정보 선택시 글자 색상 변경
    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });


    $('[data-toggle="datepicker"]').datepicker({
        format: 'yyyy-mm-dd'
    });

    $(document).on("click", ".sendBtn", function(){
        var title = $("#title").val();
        var viewType = $("#viewType").find("option:selected").val();
        var url = $("#url").val();
        var bannerImage = $("#input-piece").val();
        var startDate = $("#startDate").val();
        var endDate = $("#endDate").val();

        if( title == "" ){
            alert("제목을 입력해주세요.");
            return;
        }

        if( viewType == "" ){
            alert("표시위치를 선택해주세요");
            return;
        }

        if( url == "" ){
            alert("링크를 입력해주세요.");
            return;
        }

        if( bannerImage == "" ){
            alert("베너 이미지를 등록해주세요.");
            return;
        }

        if( startDate == "" ){
            alert("베너시작일을 입력해주세요.");
            return;
        }

        if( endDate == "" ){
            alert("베너 종료일을 입력해주세요.");
            return;
        }

        $("#saveUserForm").submit();

    });


    $(document).on("click", ".sendBtn2", function(){
        var title = $("#title").val();
        var viewType = $("#viewType").find("option:selected").val();
        var url = $("#url").val();
        var bannerImage = $("#input-piece").val();
        var startDate = $("#startDate").val();
        var endDate = $("#endDate").val();

        if( title == "" ){
            alert("제목을 입력해주세요.");
            return;
        }

        if( viewType == "" ){
            alert("표시위치를 선택해주세요");
            return;
        }

        if( url == "" ){
            alert("링크를 입력해주세요.");
            return;
        }

        if( startDate == "" ){
            alert("베너시작일을 입력해주세요.");
            return;
        }

        if( endDate == "" ){
            alert("베너 종료일을 입력해주세요.");
            return;
        }

        $("#saveUserForm").submit();

    });
});