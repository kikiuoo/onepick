$(document).ready(function(){

    if( userType != 'admin' && isDelete == '1'){
        alert("잘못된 접근입니다.");
        window.history.back(-1);
    }

    $(".allImage").text(imageCount);

    $(document).on("click", ".editBtn", function (){
        window.location.href = "/profile/edit/"+num+"/";
    });

    $(document).on("click", ".delBtn", function (){
        if( confirm("프로필 정보를 삭제하겠습니까?") == true) {
            window.location.href = "/profile/delete/" + num + "/";
        }
    });

    $(document).on("click", ".shareBtn", function (){

        var url = '';
        var textarea = document.createElement("textarea");
        document.body.appendChild(textarea);
        url = window.document.location.href;
        textarea.value = url;
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        alert("URL이 복사되었습니다.")

    });

    $(document).on("click", ".instagram, .youtube", function (){
        var b_rul = $(this).attr("data-url");

        var Url = /(http|https):\/\/((\w+)[.])+(asia|biz|cc|cn|com|de|eu|in|info|jobs|jp|kr|mobi|mx|name|net|nz|org|travel|tv|tw|uk|us)(\/(\w*))*$/i;
        var urlTest = Url.test(b_rul);

        if(!urlTest){
            alert("올바른 url이 아닙니다.");
            return false;
        }

        window.open(url);
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

        updatePick("profile", nowType );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
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
        var comment = $("#sugComment").val();

        if( audiNum == "" ){
            alert("제안할 오디션을 선택해 주세요.");
            return;
        }

        if( comment == "" ){
            alert("제안할 내용을 입력해주세요.");
            return;
        }

        saveSuggest(audiNum, comment, num, writeUID, userID);
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

        if( type == "column" ){
            alert("서비스 준비중입니다.");
            return;
        }
        window.open("/profile/print/"+type+"/"+num+"/");
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
      url: "/ajax/updatePick/",
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
      url: "/profile/ajax/saveComment/",
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
      url: "/profile/ajax/reloadComment/",
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
      url: "/profile/ajax/deleteComment/",
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
      url: "/profile/ajax/profileSuggest/",
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
