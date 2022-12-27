$(document).ready(function() {

    $(document).on("change", "#viewType", function(){
       var values = $("#viewType").find("option:selected").val();
       console.error("viewType" , viewType)

       window.location.href = "/onepickAdmin/display/audi/?audiType="+values;
    });

    $(document).on("keyup", "#search", function (){

        var search = $("#search").val();

        findAudition(search);

    });

    /*
    $(document).on("click", ".sendBtn", function(){

        var audiList = [];
        $('input:checkbox[name=profile]').each(function (index) {
            if($(this).is(":checked")==true){
                audiList.push($(this).val());
            }
        });

        var audition = audiList.join(",");

        saveRecommend( audition );
    });
    */

    $(document).on("click", "input:checkbox[name=profile]", function (){
        var value = $(this).val();
        var checked = $(this).is(":checked");

        if( checked == true ){
            saveRecommend(value, "add");
        }else{
            saveRecommend(value, "delete");
        }
    });

    $(document).on("click", ".contentBox .contentList", function(){

        $(".contentBox .contentList").removeClass("active");
        $(this).addClass("active");

        var num = $(this).attr("data-num");
        var nOrder = $(this).attr("data-order");
        active = num;
        order = nOrder;

    });

    $(document).on("click", ".circleBtn", function (){
        var cType = $(this).attr("data-type");

        if( active == "" ){
            alert("순서를 변경할 오디션을 선택해주세요.");
            return;
        }

        updateOrder( cType );
    });

});

function findAudition(word) {
    $.ajax({
        url: "/onepickAdmin/display/audi/findAudition/",
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
        url: "/onepickAdmin/display/audi/saveRecommend/",
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

function updateOrder( cType ){
    $.ajax({
        url: "/onepickAdmin/display/audi/updateOrder/",
        type: "GET",
        dataType: "json",
        data: {"cType": cType , "type" : viewType , "active" : active , "order" : order},
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
