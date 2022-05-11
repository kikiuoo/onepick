$(document).ready(function(){

    var addCount = 0;

    $(document).on("change", "#cateMain", function(){
        var cate = $(this).find("option:selected").val();

        $("#cateMain").css("color", "#1f1f1f");

        getSubCate(cate);
    })


    $(document).on("click", ".ordinaryBtn", function(){

        var disabled = $("#startDate").attr("disabled");

        alert(readOnly);

        if( readOnly == false || readOnly == undefined){
             $("#startDate").prop("disabled", true);
        }else{

        }
    });

    $(document).on("click", ".cateExpand", function (e){

        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
        }else{
            $(this).css("color", "#c0c0c0");
        }

    });

    $(document).on("change", ".ordinary", function(){

        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("../../static/image/web/textCheck_on.png")');

            $("#startDate").val("선택불가");
            $("#endDate").val("선택불가");
            $("#auditionDate").val("선택불가");
            $("#auditionTime").val("선택불가");


            $("#startDate").attr("disabled", "true");
            $("#endDate").attr("disabled", "true");
            $("#auditionDate").attr("disabled", "true");
            $("#auditionTime").attr("disabled", "true");

            if( $("#each").is(":checked") == false )
                $("#each").trigger("click");

        }else{
            $(this).css("color", "#c0c0c0");
            $(this).children("div").css("background-image", 'url("../../static/image/web/textCheck_off.png")');

            $("#startDate").val('');
            $("#endDate").val('');
            $("#auditionDate").val("");
            $("#auditionTime").val("");

            $("#startDate").removeAttr("disabled")
            $("#endDate").removeAttr("disabled")
        }
    });

    $(document).on("change", ".each", function(){

        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("../../static/image/web/textCheck_on.png")');
        }else{
            $(this).css("color", "#c0c0c0");
            $(this).children("div").css("background-image", 'url("../../static/image/web/textCheck_off.png")');
        }
    });

    $(document).on("change", "#age", function(){
        $("#age").css("color", "#1f1f1f");
    });

    $(document).on("change", "#gender", function(){
        $("#gender").css("color", "#1f1f1f");
    });

    $(document).on("change", "#career", function(){
        $("#career").css("color", "#1f1f1f");
    });


    $( "#startDate, #endDate, #auditionDate" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat : 'yy-mm-dd'
    });

    $.datepicker.regional[ "kr" ];


     $("#auditionTime").timepicker({
        timeFormat: 'HH:mm:ss',
        // year, month, day and seconds are not important
        minTime: new Date(0, 0, 0, 0, 0, 0),
        maxTime: new Date(0, 0, 0, 23, 50, 0),
        // time entries start being generated at 6AM but the plugin
        // shows only those within the [minTime, maxTime] interval
        startHour: 6,
        // the value of the first item in the dropdown, when the input
        // field is empty. This overrides the startHour and startMinute
        // options
        startTime: new Date(0, 0, 0, 0, 0, 0),
        // items in the dropdown are separated by at interval minutes
        interval: 10
    });

    //preview image
    $(document).on("change", ".upload-hidden", function (){
        var thisImage = $(this);
        var id = $(this).attr("id");
           /* file 태그 변경 */

        addCount++;

        $("#fileLabel").attr("for", "input_"+addCount);
        $(".imageBox").append('<input type="file" name="userImage[]" id="input_'+addCount+'" class="upload-hidden input_'+addCount+'">');

        /* file 이미지 처리 */
        if (!thisImage[0].files[0].type.match(/image\//)) return;//image 파일만

        var reader = new FileReader();
        reader.onload = function(e){
            var src = e.target.result;

            $(".imageBox").append('<div class="upload-display" style="background-image: url('+src+')"><div class="upload-sub" data-id="'+id+'"></div></div>')
        }

        reader.readAsDataURL(thisImage[0].files[0]);
    });

    $(document).on("click", ".upload-sub", function (){
       var id = $(this).attr("data-id");

       $("."+id).remove();
       $(this).parent().remove();

    });

    $(document).on("click", ".sendBtn", function(){
        var title = $("#title").val();
        var cate = $("#cateMain").find("option:selected");
        var subCate = $(".subCate").is(":checked");

        var ordinary = $("#ordinary").is(":checked");
        var startDate = $("#startDate").val();
        var endDate = $("#endDate").val();
        var auditionDate = $("#auditionDate").val();
        var auditionTime = $("#auditionTime").val();


        var cate = $("#age").find("option:selected");
        var cate = $("#gender").find("option:selected");
        var cate = $("#career").find("option:selected");

        if( title == "" ){
            alert("오디션 공고 제목을 입력해주세요.");
            return;
        }

        if( cate == "" || cate == undefined ){
            alert("카테고리를 선택해주세요");
            return;
        }

        if( subCate == false ){
            alert("카테고리 세부분야를 선택해주세요.");
            return;
        }

        if( ordinary == false ){
            if( startDate == ""  || endDate == "" ){
                alert("오디션 모집기간을 정확히 입력해주세요.");
                return;
            }
        }

        if( auditionDate == "" ){
            alert("오디션 날짜를 입력해주세요.");
            return;
        }

        if( auditionTime == "" ){
            alert("오디션 시간을 입력해주세요.");
            return;
        }


        if( age == "" ){
            alert("연령대를 선택해주세요.");
            return;
        }

        if( gender == "" ){
            alert("성별을 선택해주세요.");
            return;
        }

        if( career == "" ){
            alert("경력을 선택해주세요.");
            return;
        }

        $("#saveAudiForm").submit();

    });

});

function getSubCate(cate){
    $.ajax({
      url: "/audi/ajax/getSubCate/",
      type: "GET",
      dataType: "html",
      data:{"cate" : cate},

      success: function(data){
          $(".subCateBox").empty().append(data);
      },
      error: function (request, status, error){

      }
   });
}