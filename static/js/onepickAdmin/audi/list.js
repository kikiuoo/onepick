
$(document).ready(function() {
   $(document).on("change", "#viewType", function (){
     var viewType = $(this).find("option:selected").val();
       console.error("viewType" , viewType)
       window.location.href = "/onepickAdmin/audi/list/"+viewType+"/1/";
   });

   $(document).on("click", ".contentList", function (){
       var num = $(this).attr("data-num");

        window.open( "/audi/audiDetail/all/" + num + "/" );
   });

    $(document).on("click", "input:checkbox[name=recommendAudiImageEmpty]", function (e) {

        var value = $(this).val();
        var checkIndex = $(this).attr("id");
        var checked = $(this).is(":checked");

         e.preventDefault();
         e.stopPropagation();


        console.error("���� => ", checked, type, value, "recommendAudiImageEmpty")
        console.error("checkIndex => ", checkIndex)

        if (checked === true) {
            saveRecommendAudi(value, "add","recommendAudiImageEmpty", checkIndex );
        } else if(checked === false) {
            saveRecommendAudi(value, "delete", "recommendAudiImageEmpty", checkIndex);
        }
    });
    $(document).on("click", "input:checkbox[name=recommendAudiImageFull]", function (e) {
        var value = $(this).val();
        var checked = $(this).is(":checked");

        e.preventDefault();
        e.stopPropagation();

        if (checked === true) {
            saveRecommendAudi(value, "add", "recommendAudiImageFull");
        } else if(checked === false) {
            saveRecommendAudi(value, "delete", "recommendAudiImageFull");
        }
    });

    $(document).on("click", ".recommendAudi1", function (e) {
        // e.preventDefault();
        e.stopPropagation();

    });
    $(document).on("click", ".recommendAudi2", function (e) {
        // e.preventDefault();
        e.stopPropagation();
    });




   $(document).on("click", ".leftPage, .pages, .rightPage", function (){
       var page = $(this).attr("data-page");
       var listType = $(this).attr("data-type");

       if(listType === "search"){
           window.location.href = "/onepickAdmin/audi/listSearch/"+type+"/"+word+"/"+page+"/";
       }else{
           window.location.href = "/onepickAdmin/audi/list/"+type+"/"+page+"/";
       }
   });

   $(document).on("click", ".search", function(){
        var searchWord = $("#search").val();

        window.location.href = "/onepickAdmin/audi/listSearch/"+type+"/"+searchWord+"/1/";
   });

   $(document).on("click", ".listApplyView .icon", function (e){
        e.preventDefault();
        e.stopPropagation();

       var num = $(this).attr("data-num");

      window.open( "/applyList/"+num+"/" );
   });

});

function saveRecommendAudi(audiNum, rType, checkedImage, checkIndex) {
    console.error("saveRecommendAudi ���� : ", "rType-", rType, ", type - ", type, ", checkedImage - ", checkedImage, ", checkIndex - ", checkIndex)
    $.ajax({
        url: "/onepickAdmin/audi/saveRecommendAudi/",
        type: "GET",
        dataType: "json",
        data: {"num": audiNum, "rType": rType, "type": type, "checkedImage": checkedImage},
        success: function (data) {
            console.error("data.code : ", data.code)
            switch (data.code) {
             /*   case "0000" : {
                    alert("0000")
                    return window.location.reload();
                }*/
                case "add" : {
                    // alert("ĳ���� ���� ��õ �̹����� ��ϵǾ����ϴ�.")
                    return window.location.reload();
                }
                case "update" : {
                    // alert("ĳ���� ���� ��õ �̹����� �����Ǿ����ϴ�.")
                    return window.location.reload();
                }
                case "delete" : {
                    // alert("ĳ���� ���� ��õ �̹����� �����Ǿ����ϴ�.")
                    return window.location.reload();
                }
            }
        },
        error: function (request, status, error) {
            alert(error);
            window.location.reload();
        }
    });


}