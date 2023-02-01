$(document).ready(function() {
   $(document).on("change", "#viewType", function (){
       var viewType = $(this).find("option:selected").val();

       window.location.href = "/onepickAdmin/notice/list/"+viewType+"/1/";
   });

   $(document).on("click", ".contentList", function (){
       var num = $(this).attr("data-num");

       window.location.href = "/onepickAdmin/notice/viewer/"+num+"/";
   });

   $(document).on("click", ".leftPage, .pages, .rightPage", function (){
       var page = $(this).attr("data-page");

       window.location.href = "/onepickAdmin/notice/list/"+type+"/"+page+"/";
   });

   $(document).on("click", ".addBtn", function (){
       var page = $(this).attr("data-page");

       window.location.href = "/onepickAdmin/notice/write/";
   });

    $(document).on("click", ".editBtn", function (e){
        e.preventDefault();
        e.stopPropagation();

        var num = $(this).attr("data-num");
        window.location.href = "/onepickAdmin/notice/edit/"+num+"/";
    });


    $(document).on("click", ".delBtn", function (e){
        e.preventDefault();
        e.stopPropagation();

        var num = $(this).attr("data-num");

        if( confirm("공지글을 삭제하시겠습니까?") == true ){
            window.location.href = "/onepickAdmin/notice/delete/"+num+"/";
        }
    });
});