$(document).ready(function (){

    $(document).on("click", ".myProfile, .profile", function (){
        var num = $(this).attr("data-num");

        if( type == "audi" ){
            window.open("/profile/profileDetail_all/actor/" + num + "/") ;
        }else{
            window.open("/profile/profileDetail/actor/" + num + "/") ;
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


    $(window).scroll(function() {
        console.log(page + " " +$(window).scrollTop() + " " + ( $(document).height() - $(window).height() - 100 ) + " " + $(document).height() + " " +$(window).height());
        if ($(window).scrollTop() >= ($(document).height() - $(window).height())) {
            page++;

            getProfileList( page );
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

function getProfileList( page ){
    $.ajax({
      url: "/proList2/"+type+"/"+page+"/"+num+"/",
      type: "GET",
      dataType: "html",
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

