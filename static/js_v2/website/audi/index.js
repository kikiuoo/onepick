$(document).ready(function(){


    $(document).on("click", ".menuBox .menu", function (){
        var type = $(this).attr("data-type");

        window.location.href = "/audi/list/?cate_type=" + type + "&page=1&search="+search;
    });

    $(document).on("click", ".searchBox .icon", function (){
        var searchWord = $("#search").val();

        window.location.href = "/audi/list/?cate_type=" + cateType + "&page=1&search="+searchWord;
    });


    $("#search").on("keyup",function(key){
        if(key.keyCode==13){
            $(".searchBox .icon").trigger("click");
        }
    });

    // viewer 선택.
    $(document).on("click", ".audition, .audiListBox", function(){
       var num = $(this).attr("data-num");

       if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = baseUrl + "login/local/?reUrl=/audi/audiDetail/"+cateType+'/' +num +"/"
               return;
           } else {
                return;
           }
       }

       window.location.href =  baseUrl + 'audi/audiDetail/'+cateType+'/' +num +"/";
    });
    
    $(document).on("click", ".pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = baseUrl + "login/local/";
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

    $(document).on("click", ".leftPage, .pages, .rightPage", function(){
        var pages = $(this).attr("data-page");

        window.location.href = "/audi/list/?cate_type=" + cateType + "&page="+pages+"&search="+search;
    });


     $(document).on("click", ".writeBtn", function (){
        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = baseUrl + "login/local/";
               return;
           } else {
                return;
           }
       }

        window.location.href = "/audi/write/";
    });

});

window.onload = () => {
    
    if ( window.innerWidth > 767 ) {
        // pc 버전일때 적용        
        document.querySelectorAll(".audiListBox").forEach((item) => {
            item.style.gridRowEnd = `span ${item.clientHeight + 20}`;
        });
        const wrap = document.querySelector(".audiList");
        wrap.style.display = "grid";
        wrap.style.gridTemplateColumns = "repeat(auto-fill, 405px)";
        wrap.style.gridAutoRows = "1px";
    }
}

function updatePick(tableName, nowType, num){
    $.ajax({
      url: baseUrl + "common/updatePick/",
      type: "GET",
      dataType: "json",
      data:{"userID":userID, "tableName" : tableName, "nowType" : nowType, "num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });
}