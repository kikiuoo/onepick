var mainYoutube = 0;
var addListCount = 0;
$(document).ready(function (){

    // 기본정보 선택시 글자 색상 변경
    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });

    $(document).on("click", ".addBtn", function(){

        var id = $(this).attr("id");

        var addBox = "";
        var textArea = "";
        var addHtml = "";
        var array = [];

        if( id == "careerAdd" ){
            var c_cateM_val =  $("#c_cateM").find("option:selected").val();
            var c_cateS_val =  $("#c_cateS").find("option:selected").val();
            var c_cateM =  $("#c_cateM").find("option:selected").attr("data-name");
            var c_cateS =  $("#c_cateS").find("option:selected").attr("data-name");
            var c_title = $("#c_title").val();
            var c_role = $("#c_role").val();
            var saveCareer = $("#saveCareer").val();

            if( c_cateM == "" ){
                alert("경력 대분류를 선택해주세요");
                return;
            }

            if( c_cateS == "" ){
                alert("경력 세부분야를 선택해주세요");
                return;
            }

            if( c_title == "" ){
                alert("경력사항의 제목을 입력해주세요");
                return;
            }
            
            if( c_role == "" ){
                alert("경력사항의 역할을 입력해주세요");
                return;
            }

            array = saveCareer.split('|');

            if( saveCareer == "" ){ array = []; }

            var saveData =  c_cateM_val + "$" + c_cateM + "$" + c_cateS_val + "$" + c_cateS + "$" + c_title + "$" + c_role;

            if( array.indexOf(saveData) != -1 ){
                alert("이미 등록된 값입니다.");
                return;
            }

            addBox = $(".careerList");
            textArea = $("#saveCareer");
            addHtml = '<div id="list_'+addListCount+'"><input type="text" value="'+c_cateM+'" style="width: 196px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<input type="text" value="'+c_cateS+'" style="width: 196px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<input type="text" value="'+c_title+'" style="width: 288px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<input type="text" value="'+c_role+'" style="width: 358px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<div class="subBtn" id="carSub" data-id="'+addListCount+'" data-value="'+saveData+'"></div></div> ';

            // select 박스, input 박스 초기화
            $('#c_cateM').val('');
            $('#c_cateS').val('');
            $('#c_title').val('');
            $('#c_role').val('');

            $('#c_cateM').css("color", "#c0c0c0");
            $('#c_cateS').css("color", "#c0c0c0");
        }else if(id == "linkAdd"){
            var mainYoutubeCheck = $(".viewChecked #mainYoutube").is(":checked");
            var y_link = $("#y_link").val();
            var youSave = $("#youSave").val();

            if( y_link == "" ){
                alert("유튜브 영상 URL을 입력해주세요.");
                return;
            }

            array = youSave.split('|');

            if( youSave == "" ){ array = []; }

            addBox = $(".youtubeList");
            textArea = $("#youSave");

            mainYoutube = mainYoutube + 1;

            var saveData = mainYoutube + "$" + y_link;

            if( array.indexOf(saveData) != -1 ){
                alert("이미 등록된 값입니다.");
                return;
            }

            if( mainYoutubeCheck == true || array.length == 0 ){
                addHtml = '<div id="list_'+addListCount+'"><label class="textCheck mainYoutube" style="color: #ff8aae "><input type="radio" id="mainYoutube" value="'+mainYoutube+'" name="mainYoutube" checked> 메인 영상으로 설정 <div class="check" style="background-image:url(/static/image/web/textCheck_on.png)"></div></label>';
                addHtml = addHtml + '<input type="text" value="'+y_link+'" style="width: 868px; margin-right: 10px" disabled>';
                addHtml = addHtml + '<div class="subBtn" id="linkSub" data-id="'+addListCount+'" data-value="'+saveData+'"></div></div>';
            }else{
                addHtml = '<div id="list_'+addListCount+'"><label class="textCheck mainYoutube"><input type="radio" value="'+mainYoutube+'" id="mainYoutube" name="mainYoutube"> 메인 영상으로 설정 <div class="check"></div></label>';
                addHtml = addHtml + '<input type="text" value="'+y_link+'" style="width: 868px; margin-right: 10px" disabled>';
                addHtml = addHtml + '<div class="subBtn" id="linkSub" data-id="'+addListCount+'" data-value="'+saveData+'"></div></div>';
            }

            // select 박스, input 박스 초기화
            $(".viewChecked").css("color", "#c0c0c0");
            $(".viewChecked").children("div").css("background-image", 'url("/static/image/web/textCheck_off.png")');
            $('#y_link').val('');
        }else if(id == "eCareerAdd"){
            var ec_cateM =  $("#ec_cateM").find("option:selected").attr("data-name");
            var ec_cateS =  $("#ec_cateS").find("option:selected").val();
            var ec_title = $("#ec_title").val();
            var ec_role = $("#ec_role").val();
            var etcSaveCareer = $("#etcSaveCareer").val();

            if( ec_cateM == "" ){
                alert("기타경력 대분류를 선택해주세요");
                return;
            }

            if( ec_cateS == "" ){
                alert("기타경력 세부분야를 선택해주세요");
                return;
            }

            if( ec_title == "" ){
                alert("기타 경력의 상호명을 입력해주세요");
                return;
            }

            if( ec_role == "" ){
                alert("기타 경력의 역할을 입력해주세요");
                return;
            }

            array = etcSaveCareer.split('|');

            if( etcSaveCareer == "" ){ array = []; }

            var saveData =  ec_cateM + "$" + ec_cateS + "$" + ec_title + "$" + ec_role;

            if( array.indexOf(saveData) != -1 ){
                alert("이미 등록된 값입니다.");
                return;
            }

            addBox = $(".etcCareerList");
            textArea = $("#etcSaveCareer");
            addHtml = '<div id="list_'+addListCount+'"><input type="text" value="'+ec_cateM+'" style="width: 196px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<input type="text" value="'+ec_cateS+'" style="width: 196px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<input type="text" value="'+ec_title+'" style="width: 288px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<input type="text" value="'+ec_role+'" style="width: 358px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<div class="subBtn" id="eCarSub" data-id="'+addListCount+'" data-value="'+saveData+'"></div></div>';

            // select 박스, input 박스 초기화
            $('#ec_cateM').val('');
            $('#ec_cateS').val('');
            $('#ec_title').val('');
            $('#ec_role').val('');

            $('#ec_cateM').css("color", "#c0c0c0");
            $('#ec_cateS').css("color", "#c0c0c0");
        }else if(id == "foreignAdd"){
            var foreign =  $("#foreign").find("option:selected").val();
            var good =  $("#good").find("option:selected").val();
            var saveForeign = $("#saveForeign").val();

            if( foreign == "" ){
                alert("언어를 선택해주세요");
                return;
            }

            if( good == "" ){
                alert("언어 수준을 선택해주세요");
                return;
            }

            array = saveForeign.split('|');

            if( saveForeign == "" ){ array = []; }

            var saveData =  foreign + "$" + good;

            if( array.indexOf(saveData) != -1 ){
                alert("이미 등록된 값입니다.");
                return;
            }

            addBox = $(".foreignList");
            textArea = $("#saveForeign");
            addHtml = '<div id="list_'+addListCount+'"><input type="text" value="'+foreign+'" style="width: 196px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<input type="text" value="'+good+'" style="width: 116px; margin-right: 10px" disabled>';
            addHtml = addHtml + '<div class="subBtn" id="foreignSub" data-id="'+addListCount+'" data-value="'+saveData+'"></div></div>';

            // select 박스, input 박스 초기화
            $('#foreign').val('');
            $('#good').val('');
            $('#foreign').css("color", "#c0c0c0");
            $('#good').css("color", "#c0c0c0");
        }else if(id == "specialtyAdd"){
            var specialty =  $("#specialty").val();
            var saveSpecialty = $("#saveSpecialty").val();

            if( specialty == "" ){
                alert("특기를 입력해주세요.");
                return;
            }

            array = saveSpecialty.split('|');

            if( saveSpecialty == "" ){ array = []; }

            var saveData =  specialty;

            if( array.indexOf(saveData) != -1 ){
                alert("이미 등록된 값입니다.");
                return;
            }

            addBox = $("#specialty");
            textArea = $("#saveSpecialty");
            addHtml = '<div id="list_'+addListCount+'" style="display: inline-block"><input type="text" value="'+specialty+'" style="width: 226px; margin-right: 0px" disabled>';
            addHtml = addHtml + '<div class="subBtn" id="specialtySub"  data-id="'+addListCount+'" data-value="'+saveData+'" style="margin-right: 10px;"></div></div>';

            // select 박스, input 박스 초기화
            $('#specialty').val('');
        }

        array.push(saveData);
        var saveText = array.join('|');

        textArea.val(saveText);

        if(id == "specialtyAdd") {
            addBox.before(addHtml);
        }else{
            addBox.append(addHtml);
        }

        addListCount++;
    });


    $(document).on("change", "#cate_m, #c_cateM, #ec_cateM", function (){

        var id = $(this).attr("id");
        var cate = $(this).find("option:selected").val();

        if( id == "cate_m" ){
            getSubCate(cate, $("#cate_s"));
        }else if( id == "c_cateM" ){
            getSubCate(cate, $("#c_cateS"));
        }else if( id == "ec_cateM" ){
            getSubCate_etc(cate, $("#ec_cateS"));
        }

    });


    $(document).on("change", ".textCheck", function(){

        var checked = $(this).children().is(":checked");
        var id = $(this).children().attr("id");

        // 라디오 박스 처리
        if( id == "mainYoutube" ) {
            // 전체 해제
            $(".mainYoutube").css("color", "#c0c0c0");
            $(".mainYoutube").children("div").css("background-image", 'url("/static/image/web/textCheck_off.png")');
            $(".mainYoutube").children("input").removeAttr("checked");

            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_on.png")');
            $(this).children("input").attr("checked", "true");
        }else {

            if (checked == true) {
                $(this).css("color", "#ff8aae");
                $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_on.png")');
            } else {
                $(this).css("color", "#c0c0c0");
                $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_off.png")');
            }

            if (id == "notCareer") {
                if (checked == true) {
                    $("#allCarrer_y").css("color", "#c0c0c0");
                    $("#allCarrer_m").css("color", "#c0c0c0");

                    $("#allCarrer_y").val("");
                    $("#allCarrer_m").val("");
                    $("#c_cateM").val("");
                    $("#c_cateS").val("");
                    $("#c_title").val("");
                    $("#c_role").val("");

                    $("#c_cateM").attr("disabled", "true");
                    $("#c_cateS").attr("disabled", "true");
                    $("#c_title").attr("disabled", "true");
                    $("#c_role").attr("disabled", "true");
                    $("#allCareer_y").attr("disabled", "true");
                    $("#allCareer_m").attr("disabled", "true");

                    $(".careerList").empty().html('<textarea name="saveCareer" id="saveCareer"></textarea>');

                } else {
                    $("#c_cateM").removeAttr("disabled")
                    $("#c_cateS").removeAttr("disabled")
                    $("#c_title").removeAttr("disabled")
                    $("#c_role").removeAttr("disabled")
                    $("#allCareer_y").removeAttr("disabled")
                    $("#allCareer_m").removeAttr("disabled")
                }
            }
        }


    });

    $(document).on("change", "#allCareer_y", function (){
        var values = $(this).find("option:selected").val();

        if( values == "11" ){
            $("#allCareer_m").val("");
            $("#allCareer_m").attr("disabled", "true");
        }else{
            $("#allCareer_m").removeAttr("disabled");
        }
    });

    var addCount = 0;
    $(document).on("change", ".upload-hidden", function (){
        var thisImage = $(this);
        var id = $(this).attr("id");
        var type = $(this).attr("data-type");

        if(type == "mainImage"){
            $("#mainImage .addImage").css("display", "none");
            $("#mainImage").text('');

            if (!thisImage[0].files[0].type.match(/image\//)) return;//image 파일만

            var reader = new FileReader();
            reader.onload = function(e){
                var src = e.target.result;

                $("#mainImage").css("background-image", "url('"+src+"'");
            }

            reader.readAsDataURL(thisImage[0].files[0]);
        }else{
            var labelFor = "";
            var imageBox = "";
            var name = "";
            if( type == "profileImage"){
                labelFor = $("#fileLabel");
                imageBox = $(".mainImageBox .imageBox");
                name = "profileImage[]";
            }else if(type == "userImage"){
                labelFor = $("#pieceLabel");
                imageBox = $(".userImageBox .imageBox");
                name = "userImage[]";
            }

            var count = imageBox.children().length;

            if( count > 20 ){
                alert("이미지는 10장까지만 업로드가 가능합니다.");
                return;
            }

            addCount++;

            labelFor.attr("for", "input_"+addCount);
            imageBox.append('<input type="file" name="'+name+'" id="input_'+addCount+'" class="upload-hidden input_'+addCount+'" data-type="'+type+'">');

            /* file 이미지 처리 */
            if (!thisImage[0].files[0].type.match(/image\//)) return;//image 파일만

            var reader = new FileReader();
            reader.onload = function(e){
                var src = e.target.result;
                imageBox.append('<div class="upload-display" style="background-image: url('+src+')"><div class="upload-sub"  data-type="'+type+'" data-id="'+id+'"></div></div>')
            }

            reader.readAsDataURL(thisImage[0].files[0]);
        }
    });

    $(document).on("keyup", "#introduction", function(e){
       var content = $(this).val();


       if (content.length >= 1000) {
           $(this).val($(this).val().substring(0, 1000));
           alert('글자수는 1000자까지 입력 가능합니다.');
       }

       if( content.length == 0 || content == "" ){
           $(".text").text('0');
       }else{
           $(".text").text(content.length);
       }
    });

    $(document).on("click", ".subBtn", function (){
        var id = $(this).attr("id");
        var dataID = $(this).attr("data-id");
        var values = $(this).attr("data-value");

        var textArea = "";
        var array = [];

        if( id == "carSub" ){
            textArea = $("#saveCareer");
        }else if(id == "linkSub"){
            textArea = $("#youSave");
        }else if(id == "eCarSub"){
            textArea = $("#etcSaveCareer");
        }else if(id == "foreignSub"){
            textArea = $("#saveForeign");
        }else if(id == "specialtySub"){
            textArea = $("#saveSpecialty");
        }

        array = textArea.val().split("|");

        for(var i = 0; i < array.length; i++ ){
            if( array[i] == values ){
                array.splice(i,1);
                i--;
            }
        }

        var saveData = array.join('|');
        $("#list_"+dataID).remove();

        textArea.val(saveData);

    });


    $(document).on("click", ".sendBtn", function(){

        // 기본정보
        var nationality = $("#nationality").find("option:selected").val();
        var military = $("#military").find("option:selected").val();
        var finalSchool = $("#finalSchool").find("option:selected").val();
        var school = $("#school").val();
        var major = $("#major").val();

        if( nationality == "" ){
            alert("국적을 선택해주세요.");
            return;
        }
        if( military == "" ){
            alert("병역 구분을 선택해주세요.");
            return;
        }
        if( finalSchool == "" ){
            alert("최종 학력을 선택해주세요.");
            return;
        }
        if( school == "" ){
            alert("학교명을 입력해주세요.");
            return;
        }
        if( major == "" ){
            alert("학과명을 입력해주세요.");
            return;
        }

        // 신체정보
        var height = $("#height").val();
        var weight = $("#weight").val();
        var topSize = $("#topSize").find("option:selected").val();
        var bottomSize = $("#bottomSize").find("option:selected").val();
        var shoesSize = $("#shoesSize").find("option:selected").val();
        var skinColor = $("#skinColor").find("option:selected").val();
        var hairColor = $("#hairColor").find("option:selected").val();

        if( height == "" ){
            alert("키를 입력해주세요.");
            return;
        }
        if( weight == "" ){
            alert("몸무게를 입력해주세요.");
            return;
        }
        if( topSize == "" ){
            alert("상의 사이즈를 선택해주세요.");
            return;
        }
        if( bottomSize == "" ){
            alert("하의 사이즈를 선택해주세요.");
            return;
        }
        if( shoesSize == "" ){
            alert("신발 사이즈를 선택해주세요.");
            return;
        }
        if( skinColor == "" ){
            alert("피부색을 선택해주세요.");
            return;
        }
        if( hairColor == "" ){
            alert("머리색을 선택해주세요.");
            return;
        }

        // 지원 분야
        var cate_m = $("#cate_m").find("option:selected").val();
        var cate_s = $("#cate_s").find("option:selected").val();

        if( cate_m == "" ){
            alert("지원분야 대분류를 선택해주세요.");
            return;
        }
        if( cate_s == "" ){
            alert("지원분야 소분류를 선택해주세요.");
            return;
        }
        
        // 경력
        var notCareer = $("#notCareer").is(":checked");
        var saveCareer = getListData( $("#saveCareer"), 'career');

        if( notCareer == false && saveCareer == "" ){
            alert("경력을 입력해주세요.");
            return;
        }

        //이미지.
        var mainImage = $("#input-mainImage").val();

        if( mainImage == "" ){
            alert("메인 프로필 사진을 등록해주세요.");
            return;
        }

        var introduction = $("#introduction").val();

        if( notCareer == true ){
            if( introduction == "" || introduction.length < 100 ){
                alert("경력사항이 없는 경우, 자기소개를 100자 이상 작성해주세요.");
                return;
            }
        }

        getListData( $("#youSave"), 'youtube');
        getListData( $("#etcSaveCareer"), 'etcareer');
        getListData( $("#saveForeign"), 'foreign');
        getListData( $("#saveSpecialty"), 'specialty');

        $("#saveProfileForm").submit();
    });

});

function getSubCate(cate, objCate){
    $.ajax({
      url: "/profile/ajax/getSubCate/",
      type: "GET",
      dataType: "html",
      data:{"cate" : cate},

      success: function(data){
         objCate.empty().append(data);
      },
      error: function (request, status, error){

      }
   });
}


function getSubCate_etc(cate, objCate){
    $.ajax({
      url: "/profile/ajax/getSubCate_etc/",
      type: "GET",
      dataType: "html",
      data:{"cate" : cate},

      success: function(data){
         objCate.empty().append(data);
      },
      error: function (request, status, error){

      }
   });
}

function getListData( saveText, saveType){

    if( saveType == "career"){
        var c_cateM = $("#c_cateM").find("option:selected").val();
        var c_cateS = $("#c_cateS").find("option:selected").val();
        var c_title = $("#c_title").val();
        var c_role = $("#c_role").val();

        if( c_cateM != "" || c_cateS != "" || c_title != "" || c_role != "" ){
            $("#careerAdd").trigger("click");
        }
    }else  if( saveType == "youtube"){
        var y_link = $("#y_link").val();

        if( y_link != "" ){
            $("#linkAdd").trigger("click");
        }
    }else  if( saveType == "etcareer"){
        var ec_cateM = $("#ec_cateM").find("option:selected").val();
        var ec_cateS = $("#ec_cateS").find("option:selected").val();
        var ec_title = $("#ec_title").val();
        var ec_role = $("#ec_role").val();

        if( ec_cateM != "" || ec_cateS != "" || ec_title != "" || ec_role != "" ){
            $("#eCareerAdd").trigger("click");
        }
    }else  if( saveType == "foreign"){
        var foreign = $("#foreign").find("option:selected").val();
        var good = $("#good").find("option:selected").val();

        if( foreign != "" || good != "" ){
            $("#foreignAdd").trigger("click");
        }
    }else  if( saveType == "specialty"){
        var specialty = $("#specialty").val();

        if( specialty != "" ){
            $("#specialtyAdd").trigger("click");
        }
    }

    var saveContent = saveText.val();

    return saveContent;
}