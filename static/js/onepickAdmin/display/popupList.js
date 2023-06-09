$(document).ready(function() {

    $(document).on("change", "#viewType", function(){
       var values = $("#viewType").find("option:selected").val();

       window.location.href = "/onepickAdmin/display/popup/?viewType="+values+"&page=1";
    });

    $(document).on("click", ".sendBtn", function(){
       window.location.href = "/onepickAdmin/display/popup/write/";
    });

    $(document).on("click", ".editBtn", function(){
        var num = $(this).attr("data-num");

        window.location.href = "/onepickAdmin/display/popup/edit/" + num + "/";
    });

    $(document).on("click", ".delBtn", function(){
        var num = $(this).attr("data-num");

        if(confirm("등록된 배너를 삭제하겠습니까?") == true ) {
            window.location.href = "/onepickAdmin/display/popup/delete/" + num + "/";
        }
    });

    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
       var page = $(this).attr("data-page");
       var listType = $(this).attr("data-type");

       window.location.href = "/onepickAdmin/display/popup/?page="+page;
   });

});
