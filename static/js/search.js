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

       window.open( '/audi/audiDetail/all/' +num +"/" );
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


    $(window).scroll(function() {

        if( cateType == "audition") return;

        console.log($(window).scrollTop() + " " + ( $(document).height() - $(window).height() ) + " " + $(document).height() + " " +$(window).height());
        if ($(window).scrollTop() == ($(document).height() - $(window).height()- 100)) {
            page++;

            var order = $("#order").find("option:selected").val();
            var nationality = $("#nationality").find("option:selected").val();
            var geneder = $("#geneder").find("option:selected").val();
            var military = $("#military").find("option:selected").val();
            var foreign = $("#foreign").find("option:selected").val();
            var good = $("#good").find("option:selected").val();
            var age1 = $("#age1").val();
            var age2 = $("#age2").val();
            var school = $("#school").val();
            var height1 = $("#height1").val();
            var height2 = $("#height2").val();
            var career1 = $("#career1").val();

            getProfileList( order, nationality, geneder, military, foreign, good, age1, age2, school, height1, height2, career1)
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