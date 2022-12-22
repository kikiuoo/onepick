$(document).ready(function (){

    $(document).on("click", ".myProfile, .profile", function (){
        var num = $(this).attr("data-num");

        if( type == "audi" ){
            window.open( baseUrl + "profile/profileDetail_all/actor/" + num + "/") ;
        }else{
            window.open( baseUrl + "profile/profileDetail/actor/" + num + "/") ;
        }
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

        updatePick("profile", nowType, num );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }
    });


    $(document).on("change", "#listView", function(){
       var dataType = $(this).find("option:selected").val();

       window.location.href =  baseUrl + "proList/"+type+"/1/"+num+"/"+dataType+"/";
    });

    $(document).on("click", ".passBtn", function (e){
       e.preventDefault();
       e.stopPropagation();

       var num = $(this).attr("data-num");
       var image = $(this).attr("data-image");
       var comment = $(this).attr("data-comment");
       var name = $(this).attr("data-name");
       var isOn = $(this).attr("class");

       if( isOn == "passBtn passOn"){
            $(".checkView").addClass("on");
       }else{
            $(".checkView").removeClass("on");
       }

       $(".profileBox .image").css("background-image", "url('" + image + "')");
       $(".profileBox .profileName").text(name);
       $(".profileBox #comment").val(comment);
       $(".profileBox #userNum").val(num);

       $(".popupBack").css("display", "block");
    });

    $(document).on("click", ".popupClose" ,function(){
       $(".popupBack").css("display", "none");
    });

    $(document).on("click", ".prePassBtn", function (){
        var userNum = $("#userNum").val();
        var comment = $("#comment").val();

        updateApplyPick('Y', num, userNum, comment);
    });


    $(document).on("click", ".cancelPassBtn", function (){
        var userNum = $("#userNum").val();
        var comment = $("#comment").val();

        updateApplyPick('N', num, userNum, comment);
    });


    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
        var pages = $(this).attr("data-page");

        window.location.href =  baseUrl + "proList/"+type+"/"+pages+"/"+num+"/"+filter+"/";
    });

});

function updateApplyPick(pick, auditionNum, profileNum, comment){
    $.ajax({
      url:  baseUrl + "common/updateApplyPick/",
      type: "GET",
      dataType: "json",
      data:{"pick":pick, "auditionNum" : auditionNum, "profileNum" : profileNum, "comment" : comment},

      success: function(data){
          if( pick == "Y"){
              $("#pass_"+profileNum).addClass("passOn");
          } else{
              $("#pass_"+profileNum).removeClass("passOn");
          }

          $("#pass_"+profileNum).attr("data-comment", comment);
          $(".popupBack").css("display", "none");
      },
      error: function (request, status, error){

      }
   });
}

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

