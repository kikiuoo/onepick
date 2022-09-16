$(document).ready(function() {

    $(document).on("change", "#viewType", function(){
       var values = $("#viewType").find("option:selected").val();

       window.location.href = "/onepickAdmin/display/profile/?viewType="+values;
    });

    $(document).on("keyup", "#search", function (){

        var search = $("#search").val();

        findAudition(search);

    });

    $(document).on("click", "input:checkbox[name=profile]", function (){
        var value = $(this).val();
        var checked = $(this).is(":checked");

        if( checked == true ){
            saveRecommend(value, "add");
        }else{
            saveRecommend(value, "delete");
        }
    });


});

function findAudition(word) {
    $.ajax({
        url: "/onepickAdmin/display/profile/findProfile/",
        type: "GET",
        dataType: "html",
        data: {"word": word , "type" : viewType},
        success: function (data) {
            $(".searchList").empty().append(data)
        },
        error: function (request, status, error) {
            alert(error);
        }
    });
}

function saveRecommend(num, rType) {
    $.ajax({
        url: "/onepickAdmin/display/profile/saveRecommend/",
        type: "GET",
        dataType: "json",
        data: {"num": num ,"rType": rType , "type" : viewType},
        success: function (data) {
           if( data.code == "0" ){
               //alert("정상적으로 저장되었습니다.");
               window.location.reload();
           }
        },
        error: function (request, status, error) {
            alert(error);
        }
    });
}
