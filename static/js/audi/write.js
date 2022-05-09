$(document).ready(function(){

    $(document).on("change", "#cateMain", function(){

        var cate = $(this).find("option:selected").val();

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
    $('.content .upload-hidden').on('change', function(){
        var parent = $(this).parent();
        //parent.children('.upload-display').remove();

        //image 파일만
        if (!$(this)[0].files[0].type.match(/image\//)) return;

        var reader = new FileReader();
        reader.onload = function(e){
            var src = e.target.result;
            parent.prepend('<div class="upload-display"><div class="upload-thumb-wrap"><img src="'+src+'" class="upload-thumb"></div></div>');
        }

        parent.append('<input type="file" name="userImage[]" class="saveImage" value="'+ $(this).val() +'">')

        reader.readAsDataURL($(this)[0].files[0]);
    });

    $(document).on("click", "#ordinary", function (){

        var ordinary = $("#ordinary").is(":checked");

        if( ordinary == true){
            $("#startDate").attr("disabled", "true");
            $("#endDate").attr("disabled", "true");
        } else{
            $("#startDate").removeAttr("disabled")
            $("#endDate").removeAttr("disabled")
        }

    });


    $(document).on("click", ".sendBtn", function(){
        var title = $("#title").val();
        var subCate = $(".subCate").is(":checked");

        var ordinary = $("#ordinary").is(":checked");
        var startDate = $("#startDate").val();
        var endDate = $("#endDate").val();
        var auditionDate = $("#auditionDate").val();
        var auditionTime = $("#auditionTime").val();

        if( title == "" ){
            alert("오디션 공고 제목을 입력해주세요.");
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