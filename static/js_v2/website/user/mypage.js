$(document).ready(function (){

    $(document).on("click", ".editBtn", function (e){
        e.preventDefault();
        e.stopPropagation();

        var type = $(this).attr("data-type");
        var num = $(this).attr("data-num");

        if( type == "userInfo" ){
            window.location.href =  baseUrl + "users/info/update/";
        }else if( type == "profile" ){
            window.location.href =  baseUrl + "profile/edit/"+num+"/";
        }else if( type == "audition" ){
            window.location.href =  baseUrl + "audi/edit/" +num +"/";
        }

    });

    $(document).on("click", ".delBtn", function (e){
        e.preventDefault();
        e.stopPropagation();

        var num = $(this).attr("data-num");
        var type = $(this).attr("data-type");

        if( confirm("데이터를 삭제하시겠습니까?") == true ) {
            if( type == "profile" ){
                window.location.href =  baseUrl + "profile/delete/" + num + "/";
            }else if( type == "audition" ){
                window.location.href =  baseUrl + "audi/del/"+num +"/";
            }
        }
    });

    $(document).on("click", ".myProfile, .profile", function (){
        var num = $(this).attr("data-num");

        window.location.href =  baseUrl + "profile/profileDetail/actor/" + num + "/";
    });

    $(document).on("click", ".audiBtn, .audition, .regAudi", function (){
        var num = $(this).attr("data-num");

        window.location.href =  baseUrl + 'audi/audiDetail/all/' +num +"/";
    });

    $(document).on("click", ".pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
            alert("로그인 후 이용가능합니다.")
             return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).parent().attr("data-num");

        if( type == "user" ){
             updatePick("audition", nowType, num );
        }else{
             updatePick("profile", nowType, num );
        }

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }
    });

    $(document).on("click", ".mTtitle span, .audiVolunteer", function (e){
        e.preventDefault();
        e.stopPropagation();
        var type = $(this).attr("data-type");
        var num = $(this).attr("data-num");

        if( type == "notice" ){
            window.location.href =  baseUrl + "notice/list/1/";
        }else if( type == "pick" ){
            window.location.href =  baseUrl + "proList/pick/1/1/1/";
        }else if( type == "suggest" ){
            window.location.href =  baseUrl + "proList/suggest/1/1/1/";
        }else if( type == "audiProfile" ){
            window.location.href =  baseUrl + "applyList/"+num+"/";
        }else if( type == "qanda" ){
            window.location.href =  baseUrl + "qanda/list/1/";
        }

    });
});

function updatePick(tableName, nowType, num){
    $.ajax({
      url:  baseUrl + "common/updatePick/",
      type: "GET",
      dataType: "json",
      data:{"userID":userID, "tableName" : tableName, "nowType" : nowType, "num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });
}