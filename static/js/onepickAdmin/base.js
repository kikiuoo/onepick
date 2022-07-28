$(document).ready(function() {
    $(document).on("click", ".logo", function (){
       window.location.href = "/onepickAdmin/";
    });

    $(document).on("click", ".menu", function (){
       var url = $(this).attr("data-url");

       window.location.href = url;
    });

    $(document).on("click", ".logout", function(){
        logout();
    });

    $(document).on("mouseover", ".dropMenu", function (){
        $(this).children("ul").css("display", "block");
        $(this).children(".image").css("display", "block");
    });

    $(document).on("mouseleave", ".dropMenu", function (){
        $(this).children("ul").css("display", "none");
        $(this).children(".image").css("display", "none");
    });


    $(document).on("click", ".dropMenu ul li", function (e){
        e.preventDefault();
        e.stopPropagation();

        var url = $(this).attr("data-url");

        window.location.href = url;
    });
});


function logout(){
   $.ajax({
      url: "/onepickAdmin/logout/",
      type: "GET",
      dataType: "json",
      success: function(data){

          if( data.code == "0" ){
              window.location.href = "/onepickAdmin/";
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}
