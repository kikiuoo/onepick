$(document).ready(function () {

    /* Header 버튼 공통 이벤트 */
    // Logo 클릭 이벤트. (공통)
    $(document).on("click", ".header .logo", function(){
        window.location.href = "/";
    });

    // Search 클릭 이벤트. (공통)
    $(document).on("click", ".header .searchBtn", function(){
         $(".searchBox").css("display", "inline-block");
    });

    // 메뉴 버튼 이벤트 (공통)
    $(document).on("click", ".header .menu", function(){
       var url = $(this).attr("data-url");

       if(url == "#") { alert("서비스 준비중입니다."); return; }

       window.location.href = url;
    });

    /* Header 버튼 Web 이벤트 */
    // 등록 버튼 이벤트 (Web)
    $(document).on("click", ".header .registerBtn", function(){
        var display = $(".registerBox").css("display");

        if( display == "none" ){ // 화면에 표시
            $(".registerBox").css("display", "block");
        }
        else if( display == "block"){ // 화면에서 미 표시.
            $(".registerBox").css("display", "none");
        }
    });

    $(document).on("click",".header .login", function(){
        $(".loginPopup").css("display", "block");
    });

    /* Header 버튼 모바일 이벤트 */
    // menuBtn 이벤트 (모바일)
    $(document).on("click", ".header .menuBtn", function (){
        $(".menuPopup").css("display", "block");
    });


    /* Footer 버튼 공통 이벤트 */
    $(document).on("click", ".footer .companyLink span", function (){
       var url = $(this).attr("data-url");

       window.location.href = url;
    });


    /* Login Popup 버튼 공통 이벤트 */
    $(document).on("click", ".loginPopup .loginClose", function (){
       $(".loginPopup").css("display", "none");
       $(".socialLogin").css("display", "block");
       $(".onepickLogin").css("display", "none");
    });

    $(document).on("click", ".loginPopup .socialBtn", function (){
        var loginType = $(this).attr("id");

        // 각 API 구현 필요.
        if( loginType == "kakaoLogin" ){
            window.location.href = "/users/login/kakao/";
        }else if( loginType == "gogleLogin" ){
            window.location.href = "/users/login/google/";
        }else if( loginType == "appleLogin" ){

        }else if( loginType == "facebookLogin" ){

        }
    });

    $(document).on("click", ".loginPopup .sendOneLogin", function(){
        $(".socialLogin").css("display", "none");
        $(".onepickLogin").css("display", "block");
    });

    $(document).on("click", ".loginPopup .loginBtn" , function (){
       // 로그인 기능 추가.
    });

    $(document).on("click", ".loginPopup .idSearchBox span", function (){
        // 비밀번호 찾기/ id 찾기 기능 추가
        var type = $(this).attr("id");

        if( type == "findID" ){

        }else  if( type == "findPW" ) {

        }
    });

    // 기존 회원 로그인
    $(document).on("click", ".loginBtn", function (){

        var userID = $("#onepickId").val();
        var userPW = $("#onepickPW").val();

        if( userID == "" ){
            alert("아이디를 입력해 주세요.");
            return;
        }
        else if( userPW == "" ){
            alert("패스워드를 입력해 주세요.");
            return;
        }

        login(userID, userPW);

    });

    $(document).on("click", ".logout", function(){
        logout();
    });

    /* Menu Popup 버튼 mobile 이벤트 */
    $(document).on("click", ".menuPopup", function (e){
        $(".menuPopup").css("display", "none");
    });

    // 배경 클릭시 팝업닫는 기능 중 상단 이벤트가 하위 div 제어하지 않도록 이벤트 전달을 막아줌. (이벤트 중복동작 제어)
    $(document).on("click", ".menuPopup .sideMenu", function(e){
        e.preventDefault();
        e.stopPropagation();
    });

    $(document).on("click", ".menuPopup .infoBox", function(){
        var urlType = $(this).attr("id");

        if( urlType == "login" ){
            return;
        }else if( urlType == "mypick" ){
            window.location.href = "#";
        }else if( urlType == "auditonReg" ){
            window.location.href = "#";
        }else if( urlType == "profileReg" ){
            window.location.href = "#";
        }else if( urlType == "parttimeReg" ){
            window.location.href = "#";
        }else if( urlType == "advice" ){
            window.location.href = "#";
        }else if( urlType == "choice" ){
            window.location.href = "#";
        }else if( urlType == "setting" ){
            window.location.href = "#";
        }
    });
});


function login(username, password){
   $.ajax({
      url: "/users/login/local/",
      type: "POST",
      dataType: "json",
      data:{"username" : username, "password" : password},

      success: function(data){

          if( data.code == "0" ){
              window.location.href = "/";
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}


function logout(){
   $.ajax({
      url: "/users/logout/local/",
      type: "POST",
      dataType: "json",
      success: function(data){

          if( data.code == "0" ){
              window.location.href = "/";
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}