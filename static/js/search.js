$(document).ready(function(){

    $("#search").val(word);

    $(document).on("click", ".cate", function (){
        var url = $(this).attr("data-url");

        window.location.href = url;
    });

    $(document).on("click", ".audition, .audiListBox", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
            alert("로그인 후 이용가능합니다.");
            //return;
       }

       window.location.href =  '/audi/audiDetail/all/' +num +"/";
    });


    $(document).on("click", ".profile", function (){
       var num = $(this).attr("data-num");

       window.open( "/profile/profileDetail/" + cateType + "/" + num + "/" );
    });

     // 프로필 픽 기능. ( 구현 필요 )
    $(document).on("click", ".profile .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        // 기능 구현 필요
        if( userID == ""){
            alert("로그인 후 이용가능합니다.");
            return;
        }

        // 일반회원 픽기능 제한
        if( userType == "NORMAL" ||  userType == "S-NORMAL" ){
           alert("해당 기능의 권한이 없습니다.") ;
           return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).parent().attr("data-num");

        updatePick("profile", nowType, num );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }
    });

    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
        var pages = $(this).attr("data-page");

        window.location.href = "/search/"+cateType+"/"+word+"/"+pages+"/";
    });

});

function getProfileList( page, word){
    $.ajax({
      url: "/search/ajaxProfile/",
      type: "GET",
      dataType: "html",
      data:{"page":page, "word" : word },

      success: function(data){
          if( page == 1 ) {
              $(".inBox").empty().append(data);
          }else{
              $(".inBox").append(data);
          }
      },
      error: function (request, status, error){
          alert(error);
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