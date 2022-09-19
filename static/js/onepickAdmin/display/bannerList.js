$(document).ready(function() {

    $(document).on("change", "#viewType", function(){
       var values = $("#viewType").find("option:selected").val();

       window.location.href = "/onepickAdmin/display/banner/?viewType="+values+"&page=1";
    });

    $(document).on("click", ".sendBtn", function(){
       window.location.href = "/onepickAdmin/display/banner/write/";
    });

    $(document).on("click", ".editBtn", function(){
        var num = $(this).attr("data-num");

        window.location.href = "/onepickAdmin/display/banner/edit/" + num + "/";
    });

    $(document).on("click", ".delBtn", function(){
        var num = $(this).attr("data-num");

        if(confirm("등록된 배너를 삭제하겠습니까?") == true ) {
            window.location.href = "/onepickAdmin/display/banner/delete/" + num + "/";
        }
    });

});
