$(document).ready(function(){

    if( userType != 'admin' && isDelete == '1'){
        alert("잘못된 접근입니다.");
        window.history.back(-1);
    }

   // 스크랩 기능
    $(document).on("click", ".pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
            alert("로그인 후 이용가능합니다.")
             return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).attr("data-num");

        updatePick("audition", nowType, num );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }
    });

   // 오디션 지원 기능 추가
    $(document).on("click", ".auditionBtn", function(){
       // 오디션 지원 기능 추가 필요,
    });

    $(document).on("click", ".companySite", function () {
        var url = $(this).attr("data-url");

        window.open(url);
    });

    $(document).on("click", ".shareBtn", function (){
        var url = '';
        var textarea = document.createElement("textarea");
        document.body.appendChild(textarea);
        url = window.document.location.href;
        textarea.value = url;
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        alert("URL이 복사되었습니다.")
    });


    $(document).on("click", ".editBtn", function(){
        var num = $(this).attr("data-num");

        window.location.href = "/audi/edit/" +num +"/";
    });

    $(document).on("click", ".delBtn", function(){
       var num = $(this).attr("data-num");

       if(confirm("오디션을 삭제하시겠습니까?") == true){
           window.location.href = "/audi/del/"+num +"/";
       }
    });

});

function updatePick(tableName, nowType, num){
    $.ajax({
      url: "/ajax/updatePick/",
      type: "GET",
      dataType: "json",
      data:{"userID":userID, "tableName" : tableName, "nowType" : nowType, "num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });
}