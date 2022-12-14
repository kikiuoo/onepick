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
            $(this).css("border-color", "#ff8aae");
        }else{
            $(this).css("color", "#959595");
            $(this).css("border-color", "#959595");
        }

    });

    $(document).on("change", "#startDate", function (){
         $("#cateMain").css("color", "#1f1f1f");
            $(this).css("border", "1px soild #1f1f1f");
    });


    $(document).on("change", ".ordinary", function(){

        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("/static/image/web_v2/tick-square_on.png")');

            $("#startDate").val("선택불가");
            $("#endDate").val("선택불가");


            $("#startDate").attr("disabled", "true");
            $("#endDate").attr("disabled", "true");

            if( $("#each").is(":checked") == false )
                $("#each").trigger("click");

        }else{
            $(this).css("color", "#c0c0c0");
            $(this).children("div").css("background-image", 'url("/static/image/web_v2/tick-square_off.png")');

            $("#startDate").val('');
            $("#endDate").val('');

            $("#startDate").removeAttr("disabled");
            $("#endDate").removeAttr("disabled");
        }
    });

    $(document).on("change", ".notAudi", function(){

        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $("#auditionDate").val("선택불가");
            $("#auditionDate").attr("disabled", "true");

            $("#auditionDate").css("color", "#1f1f1f");
            $("#auditionDate").css("border", "1px solid #1f1f1f")
            $("#auditionDate").css("background-color", "#fff");

            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("/static/image/web_v2/tick-square_on.png")');
        }else{
            $("#auditionDate").removeAttr("disabled");
            $("#auditionDate").val("");

            $(this).css("color", "#959595");
            $(this).children("div").css("background-image", 'url("/static/image/web_v2/tick-square_off.png")');
        }
    });

    $(document).on("change", ".each", function(){

        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("/static/image/web_v2/tick-square_on.png")');
        }else{
            $(this).css("color", "#959595");
            $(this).children("div").css("background-image", 'url("/static/image/web_v2/tick-square_off.png")');
        }
    });


    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
        $(this).css("border", "1px solid #1f1f1f")
        $(this).css("background-color", "#fff");
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

    /*
    $( "#startDate, #endDate, #auditionDate" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat : 'yy-mm-dd'
    });

    $.datepicker.regional[ "kr" ];
    */

    $('[data-toggle="datepicker"]').datepicker({
        format: 'yyyy-mm-dd'
    }).on( "change", function() {
        $(this).css("color", "#1f1f1f");
        $(this).css("border", "1px solid #1f1f1f")
        $(this).css("background-color", "#fff");
    });

    //preview image
    var allImageSize = 0;
    $(document).on("change", ".upload-add", function (){
        var thisImage = $(this);
        var id = $(this).attr("id");
           /* file 태그 변경 */

        if( this.files[0].size > 9999999 ){
            alert("이미지는 10MB까지만 업로드 가능합니다.");
            return;
        }

        if( allImageSize > 29999999 ){
            alert("이미지는 1회 업로드 당 총 30MB까지만 업로드 가능합니다.");
            return;
        }

        allImageSize = allImageSize + this.files[0].size;

        addCount++;

        $("#fileLabel").attr("for", "input_"+addCount);
        $(".imageBox").append('<input type="file" name="userImage[]" id="input_'+addCount+'" class="upload-hidden  upload-add input_'+addCount+'">');

        /* file 이미지 처리 */
        if (!thisImage[0].files[0].type.match(/image\//)) return;//image 파일만

        var reader = new FileReader();
        reader.onload = function(e){
            var src = e.target.result;

            $(".imageBox").append('<div class="imageList"><div class="upload-display" style="background-image: url('+src+')"></div><div class="imageInfo">'+thisImage[0].files[0].name+'</div><div class="upload-sub" data-id="'+id+'" data-size="'+ thisImage[0].files[0].size+'"></div></div>')
        }

        reader.readAsDataURL(thisImage[0].files[0]);
    });

    $(document).on("click", ".upload-sub", function (){
       var id = $(this).attr("data-id");
       var subSize = $(this).attr("data-size");

       allImageSize = allImageSize - subSize;

       $("."+id).remove();
       $(this).parent().remove();

    });

    $(document).on("click", ".upload-sub2", function (){
       var image = $(this).attr("data-image");
       var removeImage = $("#removeImage").val();
       var remove = removeImage.split('|');
       remove.push(image);
       var removeText = remove.join("|");


       $(this).parent().remove();
       $("#removeImage").val(removeText);

    });


     $(document).on("change", "#logoLabel-file", function (){
        var thisImage = $(this);
        var id = $(this).attr("id");

        var imageTag =  $("#logoLabel .addImage");
        var imageFile = $("#logoLabel .imageInfo");
        var imageDel =  $("#logoLabel .delBtn");

        if (!thisImage[0].files[0].type.match(/image\//)) return;//image 파일만

        imageTag.text('');
        imageFile.css("color", "#1f1f1f");
        imageFile.text(thisImage[0].files[0].name);
        imageDel.css("display", "inline-block");

        var reader = new FileReader();
        reader.onload = function(e){
            var src = e.target.result;
            imageTag.css("background-image", "url('"+src+"')");
            imageTag.css("background-size", "100% auto");
        }

        reader.readAsDataURL(thisImage[0].files[0]);
    });


    $(document).on("click", ".delBtn", function (e){
        e.preventDefault();
        e.stopPropagation();

        var id = $(this).attr("data-id");

        var imageTag = $(this).parent().children(".addImage");
        var imageFile = $(this).parent().children(".imageInfo");
        var imageDel = $(this).parent().children(".delBtn");

        imageTag.css("background-image", "url('/static/image/web_v2/gallery-add.png')");
        imageTag.css("background-size", "auto");
        imageFile.css("color", "#959595");
        imageDel.css("display", "none");
        imageFile.text("이미지를 첨부하세요.");

        $("#input-"+id).val("");

    });



    $(document).on("click", ".sendBtn", function(){
        var title = $("#title").val();
        var cate = $("#cateMain").find("option:selected");
        var subCate = $(".subCate").is(":checked");

        var ordinary = $("#ordinary").is(":checked");
        var startDate = $("#startDate").val();
        var endDate = $("#endDate").val();
        var notAudi = $("#notAudi").is(":checked");
        var auditionDate = $("#auditionDate").val();


        var age = $("#age").find("option:selected");
        var gender = $("#gender").find("option:selected");
        var career = $("#career").find("option:selected");

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

        if( notAudi == false && auditionDate == "" ){
            alert("오디션 날짜를 입력해주세요.");
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
      url: baseUrl + "audi/ajax/getSubCate/",
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