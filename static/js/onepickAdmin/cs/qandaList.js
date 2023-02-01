$(document).ready(function() {
   $(document).on("click", ".contentList", function (){
       var num = $(this).attr("data-num");

       window.open("/lounge/qanda/viewer/"+num+"/");
   });

   $(document).on("click", ".leftPage, .pages, .rightPage", function (){
       var page = $(this).attr("data-page");

       window.location.href = "/onepickAdmin/cs/qanda/?page="+page;
   });
});