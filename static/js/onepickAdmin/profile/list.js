$(document).ready(function() {
   $(document).on("change", "#viewType", function (){
       var viewType = $(this).find("option:selected").val();
       window.location.href = "/onepickAdmin/profile/list/"+viewType+"/1/";
   });

   $(document).on("click", ".contentList", function (){
       var num = $(this).attr("data-num");

        window.open( "/profile/profileDetail/all/" + num + "/" );
   });

   $(document).on("click", ".leftPage, .pages, .rightPage", function (){
       var page = $(this).attr("data-page");
       var listType = $(this).attr("data-type");

       if(listType == "search"){
           window.location.href = "/onepickAdmin/profile/listSearch/"+type+"/"+word+"/"+page+"/";
       }else{
           window.location.href = "/onepickAdmin/profile/list/"+type+"/"+page+"/";
       }
   });

   $(document).on("click", ".search", function(){
        var searchWord = $("#search").val();

        window.location.href = "/onepickAdmin/profile/listSearch/"+type+"/"+searchWord+"/1/";
   });

    $(document).on("click", "input:checkbox[name=profileRecoImage]", function (e) {
        var value = $(this).val();
        var checked = $(this).is(":checked");

        e.preventDefault();
        e.stopPropagation();

        if (checked === true) {
            saveRecommendProfile(value, "add", "profile");
        } else if (checked === false) {
            saveRecommendProfile(value, "delete", "profile");
        }
    });

    $(document).on("click", ".profile", function (e) {
        // e.preventDefault();
        e.stopPropagation();
    });

});

function saveRecommendProfile(proNum, rType, checkedImage) {
    console.error("saveRecommendProfile ���� : ", "rType-", rType, ", type - ", type, ", checkedImage - ", checkedImage)
    $.ajax({
        url: "/onepickAdmin/profile/saveRecommendProfile/",
        type: "GET",
        dataType: "json",
        data: {"num": proNum, "rType": rType, "type": type, "checkedImage": checkedImage},
        success: function (data) {
            console.error("data.code : ", data.code)
            switch (data.code) {

                case "add" : {
                    // alert("ĳ���� ���� ��õ �̹����� ��ϵǾ����ϴ�.")
                    return window.location.reload();
                }
                case "update" : {
                    // alert("ĳ���� ���� ��õ �̹����� �����Ǿ����ϴ�.")
                    return window.location.reload();
                }
                case "delete" : {
                    //alert("ĳ���� ���� ��õ �̹����� �����Ǿ����ϴ�.")
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
