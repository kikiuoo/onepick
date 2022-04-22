$(document).ready(function(){
   // 목록으로 돌아가기 버튼
   $(document).on("click", ".backBtn", function (){
       window.history.go(-1);
   });

   // 스크랩 기능
    $(document).on("click", ".scrapBtn", function(){
       // 스크랩 기능 추가 필요,
    });

   // 오디션 제안 기능 추가
    $(document).on("click", ".auditionBtn", function(){
       // 오디션 제안 기능 추가 필요,
    });

    // 상세 정보 ajax 통신.
    $(document).on("click", ".subInfoCate", function (){
       var type = $(this).attr("data-type");

       $(".subInfoCate").removeClass("active");
       $(this).addClass("active");

       getsubInfo(type, num);
    });
});

function getsubInfo(type, num){
   $.ajax({
      url: "/profile/ajax/"+type+"/"+num+"/",
      type: "GET",
      dataType: "html",
      success: function(data){
         $(".subInfo").empty().html(data);
      },
      error: function (request, status, error){

      }
   });
}