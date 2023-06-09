$(document).ready(function(){

    // 메인 베너 클릭 이벤트

    // 전체보기 클릭 이벤트
    $(document).on("click", ".title span" ,function(){
        var url = $(this).attr("data-url");

        window.location.href = url;
    });

    // viewer 선택.
    $(document).on("click", ".audition, .audiListBox", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/?reUrl=/audi/audiDetail/"+cateType+'/' +num +"/"
               return;
           } else {
                return;
           }
       }

       window.location.href = '/audi/audiDetail/'+cateType+'/' +num +"/";
    });
    
    $(document).on("click", ".pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/";
               return;
           } else {
                return;
           }
       }

         // 기업회원 픽기능 제한
        if( userType == "COMPAYN" ||  userType == "S-COMPANY" ){
           alert("해당 기능의 권한이 없습니다.") ;
           return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).parent().attr("data-num");

        updatePick("audition", nowType, num );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }
    });


    $(document).on("click", ".banner", function (){
        var url = $(this).attr("data-url");
        var num = $(this).attr("data-num");

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = "/users/login/local/";
               return;
           } else {
                return;
           }
       }

        updateCount(num);

        window.open(url);
    });


    $(document).on("click", ".leftPage, .pages, .rightPage", function(){
        var pages = $(this).attr("data-page");

        window.location.href = "/audi/main/all/"+pages+"/";
    });

});

function updateCount(num){
    $.ajax({
      url: "/ajax/updateBannerCount/",
      type: "GET",
      dataType: "json",
      data:{"num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });

}

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