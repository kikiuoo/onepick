$(document).ready(function(){
        console.log("userID : ", userID)
        console.log("userType : ", userType)
//3.5 수정 

     if( userID == ""){
      // if( confirm("로그인 후에  이용가능합니다!.\n로그인 하시겠습니까?") == true){
             if( confirm("로그인 후에  이용가능합니다.\n만약 로그인 하셨던 적이 있으시다면, 재 로그인 후\n \n상단의 메뉴 > 오디션 > 마감임박순 클릭 > 오디션 지원\n \n위와 같은 경로로 오디션 지원하시기 바랍니다.") == true){
           
window.location.href = baseUrl + "login/local/?reUrl=/audi/audiDetail/actor/" + num +"/"
           return;
       } else {
           window.location.href = baseUrl ;
            return;
      }
    }


    if( userType != 'admin' && isDelete == '1'){
        alert("잘못된 접근입니다.");
        window.history.back(-1);
    }

   // 스크랩 기능
    $(document).on("click", ".pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        if( userID == ""){
            alert("로그인 후 이용가능합니다.")
             return;
        }

         // 기업회원 픽기능 제한
        if( userType == "COMPAYN" ||  userType == "S-COMPANY" ){
           alert("해당 기능의 권한이 없습니다.") ;
           return;
        }

        var nowType = $(this).attr("data-nowType");
        var num = $(this).attr("data-num");

        updatePick("audition", nowType, num );

        if( nowType == "off" ){
            $(this).attr("data-nowType", "on");
            $(this).addClass("pickOn");
        }else{
            $(this).attr("data-nowType", "off");
            $(this).removeClass("pickOn");
        }
    });

    $(document).on("click", ".companySite", function () {
        var url = $(this).attr("data-url");

        window.open(url);
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


    $(document).on("click", ".editBtn", function(){
        var num = $(this).attr("data-num");

        window.location.href = baseUrl + "audi/edit/" +num +"/";
    });

    $(document).on("click", ".delBtn", function(){
       var num = $(this).attr("data-num");

       if(confirm("오디션을 삭제하시겠습니까?") == true){
           window.location.href = baseUrl + "audi/del/"+num +"/";
       }
    });


   // 오디션 지원 기능 추가
    $(document).on("click", ".supportBtn", function(){
       // 오디션 지원 기능 추가 필요,
        if( userType == "NORMAL" || userType == "S-NORMAL" || userType == "admin") {
            $(".audiApplyBack").css("display", "block");
        }else{
            alert("권한이 없습니다.");
        }
    });

    $(document).on("click" , ".closeSPopup", function (){
        $(".audiApplyBack").css("display", "none");
    });


    $(document).on("click", ".sendProfile", function (){
        var profileCheck = $(".profileCheck:checked").val();

        if( profileCheck == "" || profileCheck == undefined ){
            alert("제출할 프로필을 선택해 주세요");
            return;
        }

        saveApply(profileCheck, num, writeUID, userID);
    });


    $(document).on("click", ".companyUrl", function (){
        var url = $(this).attr("data-url");

        window.open(url);
    });

     $(document).on("click", ".writeBtn", function (){
        if( userID == ""){
           if( confirm("로그인 후 이용가능합니다.\n로그인 하시겠습니까?") == true){
               window.location.href = baseUrl + "login/local/";
               return;
           } else {
                return;
           }
       }

        window.location.href = "/audi/write/";
    });

});



function  saveApply(profileCheck, num, writeUID, userID){
    $.ajax({
      url:  baseUrl + "audi/ajax/audiApply/",
      type: "GET",
      dataType: "json",
      data:{"profileCheck":profileCheck, "num" : num, "writeUID" : writeUID, "userID" : userID},

      success: function(data){
          if( data.code == "0"){
              alert("정상적으로 오디션 지원되었습니다.");
              $(".audiApplyBack").css("display", "none");
          }else if( data.code == "1"){
              alert(data.msg);
          }
      },
      error: function (request, status, error){

      }
   });
}


function updatePick(tableName, nowType, num){
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
