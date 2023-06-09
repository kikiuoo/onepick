$(document).ready(function(){

     if( userID == ""){
        if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
           window.location.href = baseUrl + "login/local/?reUrl=/profile/profileDetail/actor/" + num + "/";
           return;
        }else {
            window.location.href = "/";
           return;
        }
    }

    if( userType != 'admin' && isDelete == '1'){
        alert("잘못된 접근입니다.");
        window.history.back(-1);
    }

    $(".allImage").text(imageCount);

    $(document).on("click", ".editBtn", function (){
        window.location.href = baseUrl + "profile/edit/"+num+"/";
    });

    $(document).on("click", ".delBtn", function (){
        if( confirm("프로필 정보를 삭제하겠습니까?") == true) {
            window.location.href = baseUrl + "profile/delete/" + num + "/";
        }
    });

    $(document).on("click", ".shareBtn", function (){
        var shareCode = $(this).attr("data-share");
        var key = $(this).attr("data-key");
        var url = "https://myonepick.com/profile/profileShare/?num=" +  shareCode + "&key=" + key;
        var textarea = document.createElement("textarea");
        document.body.appendChild(textarea);
        textarea.value = url;
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        alert("URL이 복사되었습니다.")

    });

    $(document).on("click", ".instagram, .youtube", function (){
        var b_rul = $(this).attr("data-url");

        if( userType == 'NORMAL' && writeUID != userID ){
            alert("기업회원만 열람 가능합니다.");
            return;
        }

        var Url = /(http|https):\/\/((\w+)[.])+(asia|biz|cc|cn|com|de|eu|in|info|jobs|jp|kr|mobi|mx|name|net|nz|org|travel|tv|tw|uk|us)(\/(\w*))*$/i;
        var urlTest = Url.test(b_rul);

        var Url2 = /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
        var urlTest2 = Url2.test(b_rul);

        if(!urlTest && !urlTest2){
            alert("올바른 url이 아닙니다.");
            return false;
        }

        window.open(b_rul);
    });


   // 스크랩 기능
    $(document).on("click", ".pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
            alert("로그인 후 이용가능합니다.")
             return;
        }

         // 일반회원 픽기능 제한
        if( userType == "NORMAL" ||  userType == "S-NORMAL" ){
           alert("해당 기능의 권한이 없습니다.") ;
           return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).attr("data-num");
        var count = $(".pickCounts").text();
        count *= 1;

        updatePick("profile", nowType, num );

         if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");

            $(".pickCounts").empty().text(count + 1);
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");

            $(".pickCounts").empty().text(count - 1);
        }
    });

    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });

    $(document).on("click", ".saveComment", function (){

        if( userID == "" ){
            alert("로그인 후 이용 가능합니다.");
            return;
        }

        var comment = $("#comment").val();

        if( comment == "" ){
            alert("댓글 내용을 입력해주세요.");
            return;
        }

        $("#comment").val("");
        saveComment(comment);
    });

    $(document).on("click", ".commentDelete", function (){
       var num = $(this).attr("data-num");

       if(confirm("댓글을 삭제하시겠습니까?") == true){
           deleteComment(num);
       }
    })

    $(document).on("keyup", "#comment", function (e){
        if(e.keyCode==13) {
            $(".saveComment").trigger("click");
        }
    });

    $(document).on("click", ".rightBtn", function (){

        var nowImage = $(".nowImage").text();
        var viewImageCount = (nowImage * 1) + 1;

        if( viewImageCount > imageCount ) return;

        viewImage(viewImageCount);
    });

    $(document).on("click", ".leftBtn", function (){

        var nowImage = $(".nowImage").text();
        var viewImageCount = (nowImage * 1) - 1;

        if( viewImageCount < 1 ) return;

        viewImage(viewImageCount);
    });


    $(document).on("click", ".mainImage, .imageBox img", function (){
        var viewImageCount = $(this).attr("data-id");

        $(".popupBack").css("display", "block");

        viewImage(viewImageCount);
    });

    $(document).on("click", ".closePopup", function (e){
        e.preventDefault();
        e.stopPropagation();

        $(".popupBack").css("display", "none");
    });


   // 오디션 제안 기능 추가
    $(document).on("click", ".auditionBtn", function(){

        if( userType == "COMPANY" || userType == "admin") {
            $(".suggestBack").css("display", "block");
        }else{
            alert("권한이 없습니다.");
        }
    });

    $(document).on("click" , ".closeSPopup", function (){
        $(".suggestBack").css("display", "none");
    });


    $(document).on("click", ".suggestBtn", function (){
        var audiNum = $("#audi").find("option:selected").val();

        if( audiNum == "" ){
            alert("제안할 오디션을 선택해 주세요.");
            return;
        }

        saveSuggest(audiNum, "", num, writeUID, userID);
    });

    $(document).on("click", ".printBtn", function (){
       var css = $(".vector").css("display");

       if( css == "block" ){
           $(".vector").css("display", "none");
       }else{
           $(".vector").css("display", "block");
       }
    });


    $(document).on("click", ".vector span" , function (e){
        e.preventDefault();
        e.stopPropagation();

        var type = $(this).attr("data-type");
        var shareCode = $(this).attr("data-share");
        var key = $(this).attr("data-key");

        window.open("/profile/print/"+type+"/"+num+"/?share=" + shareCode + "&key=" + key);
    });

});

function viewImage(viewImageCount) {

        if( viewImageCount < imageCount ){
            $(".rightBtn").removeClass("rightOff");
            $(".rightBtn").addClass("rightOn");
        }else if( viewImageCount == imageCount ){
            $(".rightBtn").removeClass("rightOn");
            $(".rightBtn").addClass("rightOff");
        }

        if( viewImageCount == 1 ){
            $(".rightBtn").removeClass("leftOn");
            $(".leftBtn").addClass("leftOff");
        }else if( viewImageCount <= imageCount ){
            $(".rightBtn").removeClass("leftOff");
            $(".leftBtn").addClass("leftOn");
        }

        var viewImage = $("#image_"+viewImageCount).attr("data-image");


        $(".viewImage").attr("src", viewImage);


        var imageX = $(".viewImage").width() / 2;
        var imageY = $(".viewImage").height()/ 2;

        $(".viewImage").css("margin-left", "-"+imageX+"px");
        $(".viewImage").css("margin-top", "-"+imageY+"px");

        $(".nowImage").text(viewImageCount);
}


function updatePick(tableName, nowType){
    $.ajax({
      url: baseUrl + "common/updatePick/",
      type: "GET",
      dataType: "json",
      data:{"userID":userID, "tableName" : tableName, "nowType" : nowType, "num" : num},

      success: function(data){

      },
      error: function (request, status, error){

      }
   });
}


function saveComment(comment){
    $.ajax({
      url:  baseUrl + "profile/ajax/saveComment/",
      type: "GET",
      dataType: "json",
      data:{"comment" : comment, "num" : num},

      success: function(data){
          if( data.code == "0"){
            reloadComment();
          }
      }
      ,
      error: function (request, status, error){

      }

   });
}

function reloadComment(){
    $.ajax({
      url: baseUrl + "profile/ajax/reloadComment/",
      type: "GET",
      dataType: "html",
      data:{ "num" : num},

      success: function(data){
          $(".commentList").empty().append(data);
      }
      ,
      error: function (request, status, error){

      }

   });
}

function deleteComment(num){
    $.ajax({
      url: baseUrl + "profile/ajax/deleteComment/",
      type: "GET",
      dataType: "json",
      data:{ "num" : num },

      success: function(data){
          if( data.code == "0"){
            reloadComment();
          }
      }
      ,
      error: function (request, status, error){

      }

   });
}


function saveSuggest(audiNum, comment, num, writeUID, userID){
    $.ajax({
      url: baseUrl + "profile/ajax/profileSuggest/",
      type: "GET",
      dataType: "json",
      data:{"audiNum":audiNum, "comment" : comment, "num" : num, "writeUID" : writeUID, "userID" : userID},

      success: function(data){
          if( data.code == "0"){
              alert("정상적으로 오디션 제안되었습니다.");
              $("#audi").val("");
              $("#sugComment").val("");
              $(".suggestBack").css("display", "none");
          }
      },
      error: function (request, status, error){

      }
   });
}
