$(document).ready(function() {
   $(document).on("change", "#viewType", function (){
       var viewType = $(this).find("option:selected").val();

       window.location.href = "/onepickAdmin/audi/list/"+viewType+"/1/";
   });

   $(document).on("click", ".contentList", function (){
       var num = $(this).attr("data-num");

        window.open( "/audi/audiDetail/all/" + num + "/" );
   });

   $(document).on("click", ".leftPage, .pages, .rightPage", function (){
       var page = $(this).attr("data-page");
       var listType = $(this).attr("data-type");

       if(listType == "search"){
           window.location.href = "/onepickAdmin/audi/listSearch/"+type+"/"+word+"/"+page+"/";
       }else{
           window.location.href = "/onepickAdmin/audi/list/"+type+"/"+page+"/";
       }
   });

   $(document).on("click", ".search", function(){
        var searchWord = $("#search").val();

        window.location.href = "/onepickAdmin/audi/listSearch/"+type+"/"+searchWord+"/1/";
   });

});