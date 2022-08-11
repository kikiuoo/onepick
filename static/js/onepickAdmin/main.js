$(document).ready(function() {

    $(document).on("click", ".typeBtn", function (){
        var type = $(this).attr("data-type");

        $(".typeBtn").removeClass("selected");
        $(this).addClass("selected");

        getGraph( "user", type );
    });

    $(document).on("click", ".typeBtn2", function (){
        var type = $(this).attr("data-type");

        $(".typeBtn2").removeClass("selected");
        $(this).addClass("selected");

        getGraph( "connect", type );
    });


    $(document).on("click", ".typeBtn3", function (){
        var type = $(this).attr("data-type");

        $(".typeBtn3").removeClass("selected");
        $(this).addClass("selected");

        getGraph( "login", type );
    });
});


function getGraph(dataType, type){
   $.ajax({
      url: "/onepickAdmin/ajax/getGraph/",
      type: "GET",
      dataType: "html",
      data:{"dataType" : dataType, "type" : type},
      success: function(data){
        if( dataType == "user" ){
            $("#userBox").empty().append(data);
        }else if( dataType == "connect" ){
            $("#connectBox").empty().append(data);
        }else if( dataType == "login" ){
            $("#loginBox").empty().append(data);
        }
      },
      error: function (request, status, error){

      }
   });
}
