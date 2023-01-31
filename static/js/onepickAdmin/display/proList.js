$(document).ready(function() {

    // 문서에서 viewType이 변경되면, 이벤트 바인드( : on)
    // viewType의 하위요소에서 select  box 선택값 가져오기

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
      console.error("눌림" , viewType)

       console.log('value : ' +value);
       console.log('checked : ' +checked);

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

// 체크 선택하면
function saveRecommend(num, rType) {

    $.ajax({
        url: "/onepickAdmin/display/profile/saveRecommend/",
        type: "GET",
        dataType: "json",
        data: {"num": num ,"rType": rType , "type" : viewType},
        success: function (data) {
           if( data.code == "0" ){
               // alert("정상적으로 저장되었습니다.");
               window.location.reload();
           }
        },
        error: function (request, status, error) {
            alert(error);
        }
    });
}
