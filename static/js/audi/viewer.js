$(document).ready(function(){
    // 목록으로 돌아가기 버튼
   $(document).on("click", ".backBtn", function (){
       window.history.go(-1);
   });

   // 스크랩 기능
    $(document).on("click", ".scrapBtn", function(){
       // 스크랩 기능 추가 필요,
    });

   // 오디션 지원 기능 추가
    $(document).on("click", ".auditionBtn", function(){
       // 오디션 지원 기능 추가 필요,
    });

    $(document).on("click", ".urlLink", function () {
        var url = $(this).attr("data-url");

        window.open(url);
    });
});