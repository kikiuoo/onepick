$(document).ready(function(){
      // 기본정보 선택시 글자 색상 변경
    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });

    $(document).on("change", ".order", function(){
        var orderType = $(".order").find("option:selected").val();

        window.location.href = "/profile/list/" + cateType + "/" + orderType +"/";
    });

    $(document).on("click", ".profile", function (){
       var num = $(this).attr("data-num");

       // 기능 구현 필요
        if( userID == ""){
            alert("로그인 후 이용가능합니다.");
            return;
        }

       window.location.href =  "/profile/profileDetail/" + cateType + "/" + num + "/";
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

     $(document).on("change", "#order2", function(){

        var order = "";
        if( $("#order2.mobileNone").css("display") == "block" ){
            order = $("#order2").find("option:selected").val();
        }else{
            order = $("#order").find("option:selected").val();
        }

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

        window.location.href = "/profile/list/"+cateType+"/1/?order="+order+"&nationality="+nationality+"&geneder="+geneder
                                +"&military="+military+"&foreign="+foreign+"&good="+good+"&age1="+age1+"&age2="+age2
                                +"&school="+school+"&height1="+height1+"&height2="+height2+"&career1="+career1;
    });



    $(document).on("click", ".filterSave", function(){

        var order = "";
        if( $("#order2.mobileNone").css("display") == "block" ){
            order = $("#order2").find("option:selected").val();
        }else{
            order = $("#order").find("option:selected").val();
        }

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

        window.location.href = "/profile/list/"+cateType+"/1/?order="+order+"&nationality="+nationality+"&geneder="+geneder
                                +"&military="+military+"&foreign="+foreign+"&good="+good+"&age1="+age1+"&age2="+age2
                                +"&school="+school+"&height1="+height1+"&height2="+height2+"&career1="+career1;
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

        window.location.href = "/profile/list/"+cateType+"/1/";
    });

    $(document).on("click", ".filterBtn", function (){
        $(".filterBox").css("display", "block");
    });

    $(document).on("click", ".filterSave, .closeBtn", function (){
        //$(".filterBox").css("display", "none");
    });

    /*
        2022-08-23 무한스크롤 -> 페이징
    var pageHeight = $(document).height() - $(window).height();
    $(window).scroll(function() {
        var scrollH = $(window).scrollTop();
        var pageH = ( pageHeight * page ) - 100;

        console.log(page + " " +scrollH + " " + pageH);
        if (scrollH >= pageH) {
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

    */

    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
        var pages = $(this).attr("data-page");

        var order = "";
        if( $("#order2.mobileNone").css("display") == "block" ){
            order = $("#order2").find("option:selected").val();
        }else{
            order = $("#order").find("option:selected").val();
        }

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

        window.location.href = "/profile/list/"+cateType+"/"+pages+"/?order="+order+"&nationality="+nationality+"&geneder="+geneder
                                +"&military="+military+"&foreign="+foreign+"&good="+good+"&age1="+age1+"&age2="+age2
                                +"&school="+school+"&height1="+height1+"&height2="+height2+"&career1="+career1;

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