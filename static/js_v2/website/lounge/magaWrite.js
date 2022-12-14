$(document).ready(function(){
    $(document).on("click", ".sendBtn2", function(){

        var title = $("#title").val();
        var content = $("#content").val();


        if( title == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        if( content == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        $("#saveQanda").submit();
    });


    // 기본정보 선택시 글자 색상 변경
    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });


    var addCount = 0;
     //preview image
    var allImageSize = 0;
    $(document).on("change", ".upload-hidden", function (){
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
        $(".imageBox").append('<input type="file" name="userImage[]" id="input_'+addCount+'" class="upload-hidden input_'+addCount+'">');

        /* file 이미지 처리 */
        if (!thisImage[0].files[0].type.match(/image\//)) return;//image 파일만

        var reader = new FileReader();
        reader.onload = function(e){
            var src = e.target.result;

            $(".imageBox").append('<div class="upload-display" style="background-image: url('+src+')"><div class="upload-sub" data-id="'+id+'" data-size="'+ thisImage[0].files[0].size+'"></div></div>')
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

});
