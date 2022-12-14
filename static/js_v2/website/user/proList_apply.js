$(document).ready(function (){

     // 기본정보 선택시 글자 색상 변경
    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });

    $(document).on("click", ".myProfile, .profile", function (){
        var num = $(this).attr("data-num");
        window.open( baseUrl + "profile/profileDetail_all/actor/" + num + "/") ;
    });

    $(document).on("click", ".pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
            alert("로그인 후 이용가능합니다.")
             return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).parent().attr("data-num");

        updatePick("profile", nowType, num );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }
    });

    $(document).on("click", ".passBtn", function (e){
       e.preventDefault();
       e.stopPropagation();

       var num = $(this).attr("data-num");
       var image = $(this).attr("data-image");
       var comment = $(this).attr("data-comment");
       var name = $(this).attr("data-name");
       var isOn = $(this).attr("class");

       if( isOn == "passBtn passOn"){
            $(".checkView").addClass("on");
       }else{
            $(".checkView").removeClass("on");
       }

       $(".profileBox .image").css("background-image", "url('" + image + "')");
       $(".profileBox .profileName").text(name);
       $(".profileBox #comment").val(comment);
       $(".profileBox #userNum").val(num);

       $(".popupBack").css("display", "block");
    });

    $(document).on("click", ".popupClose" ,function(){
       $(".popupBack").css("display", "none");
    });

    $(document).on("click", ".prePassBtn", function (){
        var userNum = $("#userNum").val();
        var comment = $("#comment").val();

        updateApplyPick('Y', num, userNum, comment);
    });


    $(document).on("click", ".cancelPassBtn", function (){
        var userNum = $("#userNum").val();
        var comment = $("#comment").val();

        updateApplyPick('N', num, userNum, comment);
    });

    $(document).on("click", ".filterBtn", function (){

        if( $(".filterBox").css("display") == "block" ){
            $(".filterBox").css("display", "none");
            $(".filterSave").css("display", "none");
            $(".filterBtn span").css("transform", "rotate(0deg)");
        }else{
            $(".filterBox").css("display", "block");
            $(".filterSave").css("display", "inline-block");
            $(".filterBtn span").css("transform", "rotate(180deg)");
        }
    });


    $(document).on("click", ".resetBox", function(){

        $("#nationality").val("");
        $("#geneder").val("");
        $("#military").val("");
        $("#foreign").val("");
        $("#good").val("");
        $("#age1").val("");
        $("#age2").val("");
        $("#school").val("");
        $("#height1").val("");
        $("#height2").val("");
        $("#career1").val("");
        $("#career2").val("");

        $("#nationality").css("color", "#c0c0c0");
        $("#geneder").css("color", "#c0c0c0");
        $("#military").css("color", "#c0c0c0");
        $("#foreign").css("color", "#c0c0c0");
        $("#good").css("color", "#c0c0c0");

        $(".ageRadio").prop("checked", false);
        $(".heightRadio").prop("checked", false);
        $(".careerRadio").prop("checked", false);

        $(".foreFindList").empty().append('<textarea name="foreSpec" id="foreSpec"></textarea>');
        $(".specFindList").empty().append('<textarea name="findSpec" id="findSpec"></textarea>');
        $(".tagFindList").empty().append('<textarea name="tagSpec" id="tagSpec"></textarea>');

    });

     $(document).on("click", ".ageRadio", function (){
        $("#age2").val('');
        $("#age1").val('');
    });

    $(document).on("keyup", "#age2, #age1", function (){
        $(".ageRadio").prop("checked", false);
    });


    $(document).on("click", ".heightRadio", function (){
        $("#height1").val('');
        $("#height2").val('');
    });

    $(document).on("keyup", "#height1, #height2", function (){
        $(".heightRadio").prop("checked", false);
    });

    $(document).on("click", ".careerRadio", function (){
        $("#career1").val('');
        $("#career2").val('');
    });

    $(document).on("keyup", "#career1, #career2", function (){
        $(".careerRadio").prop("checked", false);
    });

    $(document).on("change", "#specialty", function (){
       var specialty = $("#specialty").find(":selected").val();

       find_sub_specialty(specialty);
    });

    $(document).on("click", ".closeBtn", function (){
        $(".filterBox").css("display", "none");
    });


    var addListCount = 0;
    $(document).on("change", ".addCondition", function (){

        var id = $(this).attr("id");

        var addBox = "";
        var textArea = "";
        var addHtml = "";
        var array = [];

        if( id == "good") {

            var foreign = $("#foreign").find(":selected").val();
            var good = $("#good").find(":selected").val();
            var saveForeign = $("#foreSpec").val();

            if (foreign == "" || good == "") {
                alert("언어를 선택해주세요.");
                return;
            }

            array = saveForeign.split('|');

            if( saveForeign == "" ){ array = []; }

            var saveData =  foreign + "$" + good;

            if( array.indexOf(saveData) != -1 ){
                alert("이미 등록된 값입니다.");
                return;
            }

            addBox = $(".foreFindList");
            textArea = $("#foreSpec");
            addHtml = '<div class="foreFind" id="list_'+addListCount+'">'+foreign+' > '+good+'<span class="subBtn" id="foreSub" data-val="'+saveData+'" data-id="'+addListCount+'"></span></div>';

            // select 박스, input 박스 초기화
            $('#foreign').val('');
            $('#good').val('');
            $('#foreign').css("color", "#c0c0c0");
            $('#good').css("color", "#c0c0c0");
        }else if( id == "spec_sub") {
            var specialty = $("#specialty").find(":selected").val();
            var spec_sub = $("#spec_sub").find(":selected").val();
            var saveForeign = $("#findSpec").val();

            if (specialty == "" || spec_sub == "") {
                alert("특기를 선택해주세요.");
                return;
            }
            array = saveForeign.split('|');

            if( saveForeign == "" ){ array = []; }
            var saveData =  specialty + "$" + spec_sub;
            if( array.indexOf(saveData) != -1 ){
                alert("이미 등록된 값입니다.");
                return;
            }

            addBox = $(".specFindList");
            textArea = $("#findSpec");
            addHtml = '<div class="specFind" id="list_'+addListCount+'">'+specialty+' > '+spec_sub+'<span class="subBtn" id="specSub" data-val="'+saveData+'" data-id="'+addListCount+'"></span></div>';

            // select 박스, input 박스 초기화
            $('#specialty').val('');
            $('#spec_sub').val('');
            $('#specialty').css("color", "#c0c0c0");
            $('#spec_sub').css("color", "#c0c0c0");
        }else if( id == "tag") {
            var tag = $("#tag").find(":selected").val();
            var saveForeign = $("#tagSpec").val();

            if (tag == "") {
                alert("태그를 선택해주세요.");
                return;
            }
            array = saveForeign.split('|');

            if( saveForeign == "" ){ array = []; }
            var saveData =  tag;
            if( array.indexOf(saveData) != -1 ){
                alert("이미 등록된 값입니다.");
                return;
            }

            addBox = $(".tagFindList");
            textArea = $("#tagSpec");
            addHtml = '<div class="tagFind" id="list_'+addListCount+'">'+tag+'<span class="subBtn" id="tagSub" data-val="'+saveData+'" data-id="'+addListCount+'"></span></div>';

            // select 박스, input 박스 초기화
            $('#tag').val('');
            $('#tag').css("color", "#c0c0c0");
        }

        array.push(saveData);
        var saveText = array.join('|');

        textArea.val(saveText);
        addBox.append(addHtml);

    });

    $(document).on("click", ".subBtn", function (){
        var id = $(this).attr("id");
        var dataID = $(this).attr("data-id");
        var values = $(this).attr("data-val");

        var textArea = "";
        var array = [];

        if( id == "tagSub" ){
            textArea = $("#tagSpec");
        }else if(id == "foreSub"){
            textArea = $("#foreSpec");
        }else if(id == "specSub"){
            textArea = $("#findSpec");
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

    $(document).on("click", ".filterSave", function(){
        $("#page").val("1");

        $("#sendForm").submit();
    });

    $(document).on("change", "#listView", function(){
        $("#page").val("1");

        $("#sendForm").submit();
    });


    $(document).on("click", ".leftPage, .pages, .rightPage", function (){
        var pages = $(this).attr("data-page");
        $("#page").val(pages);
        $("#sendForm").submit();
    });

});

function updateApplyPick(pick, auditionNum, profileNum, comment){
    $.ajax({
      url:  baseUrl + "ajax/updateApplyPick/",
      type: "GET",
      dataType: "json",
      data:{"pick":pick, "auditionNum" : auditionNum, "profileNum" : profileNum, "comment" : comment},

      success: function(data){
          if( pick == "Y"){
              $("#pass_"+profileNum).addClass("passOn");
          } else{
              $("#pass_"+profileNum).removeClass("passOn");
          }

          $("#pass_"+profileNum).attr("data-comment", comment);
          $(".popupBack").css("display", "none");
      },
      error: function (request, status, error){

      }
   });
}

function updatePick(tableName, nowType, num){
    $.ajax({
      url:  baseUrl + "ajax/updatePick/",
      type: "GET",
      dataType: "json",
      data:{"userID":userID, "tableName" : tableName, "nowType" : nowType, "num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });
}

function find_sub_specialty(specialty){
    $.ajax({
      url:  baseUrl + "profile/ajax/getSubSpecialty2/",
      type: "GET",
      dataType: "html",
      data:{"specialty" : specialty},

      success: function(data){
         $("#spec_sub").empty().append(data);
      },
      error: function (request, status, error){

      }
   });
}