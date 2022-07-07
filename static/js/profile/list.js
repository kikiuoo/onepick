$(document).ready(function(){

    $(document).on("change", ".order", function(){
        var orderType = $(".order").find("option:selected").val();

        window.location.href = "/profile/list/" + cateType + "/" + orderType +"/";
    });

    $(document).on("click", ".profile", function (){
       var num = $(this).attr("data-num");

       window.location.href = "/profile/profileDetail/" + cateType + "/" + num + "/" ;
    });

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


    // 필터 적용
    $(document).on("change", "#order, #nationality, #geneder, #military, #foreign, #good, #order2, #career1", function(){

        var index = $(this).find("option:selected").index();

        if( index == 0 && ( $(this).attr("id") != 'order' && $(this).attr("id") != 'order2' ) ){
            $(this).css("color", "#c0c0c0");
        }else{
            $(this).css("color", "#1f1f1f");
        }

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
        var career1 = $("#career1").find("option:selected").val();

        page = 1;

        getProfileList( order, nationality, geneder, military, foreign, good, age1, age2, school, height1, height2, career1);

    });

    $(document).on("keyup", "#age1, #age2, #school, #height1, #height2", function(){

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
        var career1 = $("#career1").find("option:selected").val();

        page = 1;

        getProfileList( order, nationality, geneder, military, foreign, good, age1, age2, school, height1, height2, career1);

    });


    $(document).on("click", ".resetBox", function(){

        $("#nationality").val("");
        $("#geneder").val("");
        $("#military").val("");
        $("#foreign").val("");
        $("#good").val("");
        $("#age1").val("");
        $("#age2").val("");
        $("#school").val("");
        $("#height1").val("");
        $("#height2").val("");
        $("#career1").val("");

        $("#nationality").css("color", "#c0c0c0");
        $("#geneder").css("color", "#c0c0c0");
        $("#military").css("color", "#c0c0c0");
        $("#foreign").css("color", "#c0c0c0");
        $("#good").css("color", "#c0c0c0");

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

        page = 1;

        getProfileList( order, nationality, geneder, military, foreign, good, age1, age2, school, height1, height2, career1);
    });

    $(document).on("click", ".filterBtn", function (){
        $(".filterBox").css("display", "block");
    });

    $(document).on("click", ".filterSave, .closeBtn", function (){
        $(".filterBox").css("display", "none");
    });


    $(window).scroll(function() {
        console.log(page + " " +$(window).scrollTop() + " " + ( $(document).height() - $(window).height() - 100 ) + " " + $(document).height() + " " +$(window).height());
        if ($(window).scrollTop() >= ($(document).height() - $(window).height())) {
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

function getProfileList( order, nationality, geneder, military, foreign, good, age1, age2, school, height1, height2, career1){
    $.ajax({
      url: "/profile/ajax/getProfile/",
      type: "GET",
      dataType: "html",
      data:{"order":order, "nationality" : nationality, "geneder" : geneder, "military" : military,
            "foreign":foreign, "good" : good, "age1" : age1, "age2" : age2, "school":school,
            "height1" : height1, "height2" : height2, "career1" : career1, "page":page, "cate_type":cateType },

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