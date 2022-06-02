$(document).ready(function (){

    $(document).on("click", ".editBtn", function (e){
        e.preventDefault();
        e.stopPropagation();

        var type = $(this).attr("data-type");

        if( type == "userInfo" ){
            window.location.href = "/users/info/update/";
        }else if( type == "profile" ){
            var num = $(this).attr("data-num");
            window.location.href = "/profile/edit/"+num+"/";
        }

    });

    $(document).on("click", ".delBtn", function (e){
        e.preventDefault();
        e.stopPropagation();

        var num = $(this).attr("data-num");
        var type = $(this).attr("data-type");

        if( confirm("데이터를 삭제하시겠습니까?") == true ) {
            if( type == "profile" ){
                window.location.href = "/profile/delete/" + num + "/";
            }
        }
    });

    $(document).on("click", ".myProfile", function (){
        var num = $(this).attr("data-num");

        window.open("/profile/profileDetail/actor/" + num + "/") ;
    });

    $(document).on("click", ".audiBtn, .audition", function (){
        var num = $(this).attr("data-num");

        window.open('/audi/audiDetail/all/' +num +"/") ;
    });

     $(document).on("click", ".pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
            alert("로그인 후 이용가능합니다.")
             return;
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