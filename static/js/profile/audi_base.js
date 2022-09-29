$(document).ready(function(){

    // 카테고리 선택
    $(document).on("click", ".cate", function(){
        var url = $(this).attr("data-url");
        $("#page").val("1");
        $("#cate").val(url);

        $("#sendForm").submit();
    });

});