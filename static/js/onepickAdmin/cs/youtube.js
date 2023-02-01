$(document).ready(function() {

     $(document).on("click", ".sendBtn", function (){

         if( confirm("유튜브 정보를 다시 체크하시겠습니까??\n로그인 기준 21/01/01 이후 접속자만 체크됩니다.") == true){
             $(".popup").css("display", "block");
             checkYoutube();
         }
     });

});


function checkYoutube(){
    $.ajax({
      url: "/onepickAdmin/cs/checkYoutube/",
      type: "GET",
      dataType: "json",
      success: function(data){
          window.location.reload();
      },
      error: function (request, status, error){
          alert(error);
      }
   });
}

