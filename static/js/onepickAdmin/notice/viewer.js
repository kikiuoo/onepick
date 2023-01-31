$(document).ready(function() {

    $(document).on("click", ".editBtn", function (){
        window.location.href = "/onepickAdmin/notice/edit/"+num+"/";
    });


    $(document).on("click", ".delBtn", function (){

        if( confirm("공지글을 삭제하시겠습니까?") == true ){
            window.location.href = "/onepickAdmin/notice/delete/"+num+"/";
        }

    });
});
