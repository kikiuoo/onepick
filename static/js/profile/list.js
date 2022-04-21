$(document).ready(function(){

    $(document).on("change", ".order", function(){
        var orderType = $(".order").find("option:selected").val();

        window.location.href = "/profile/list/" + cateType + "/" + orderType +"/";
    });

    $(document).on("click", ".profile", function (){
       var num = $(this).attr("data-num");

       window.location.href = "/profile/profileDetail/" + cateType + "/" + num + "/" ;
    });

});