var baseUrl = "/";

$(document).ready(function () {

    /* Header 버튼 공통 이벤트 */
    // Logo 클릭 이벤트. (공통)
    $(document).on("click", ".header .logo", function(){
        window.location.href = baseUrl;
    });

    // 메뉴 버튼 이벤트 (공통)
    $(document).on("click", ".header .menu, .menuCate", function(){
       var url = $(this).attr("data-url");
       var type = $(this).attr("data-type");

       if(url == "#") { alert("서비스 준비중입니다."); return; }

       if( type == "open" ){
           window.open( url );
       }else{
           window.location.href = baseUrl +  url;
       }

    });

    /* Header 버튼 Web 이벤트 */
    $(document).on("click",".login", function(){
        window.location.href =  baseUrl +  "login/local/";
    });

    /* Header 버튼 Web 이벤트 */
    $(document).on("click",".join", function(){
        window.location.href =  baseUrl +  "login/joinView/";
    });

    /* Header 버튼 모바일 이벤트 */
    // menuBtn 이벤트 (모바일)
    $(document).on("click", ".header .menuBtn", function (){
        $(".menuPopup").css("display", "block");
    });


    /* Footer 버튼 공통 이벤트 */
    $(document).on("click", ".footer .companyLink span", function (){
       var url = $(this).attr("data-url");

       window.open(url);
    });

    $(document).on("click", ".footer .link_sns", function (){
       var url = $(this).attr("data-url");

       window.open(url);
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

    $(document).on("click", ".mypage", function(){

       if( userID == null || userID == ""){
            alert("로그인 후 이용가능합니다.");
            return;
        }

        if( userType == "COMPANY" || userType == "S-COMPANY" ){
            window.location.href = baseUrl +  "users/mypage/company/";
        }else{
            window.location.href = baseUrl +  "users/mypage/user/";
        }

    });

    $(document).on("keyup", "input, textarea", function (){
        var value = $(this).val();

        if( value == "" ){
            $(this).css("background-color" , "#f8f8f8");
            $(this).css("border" , "0px solid #fff");
        }else{
            $(this).css("background-color" , "#fff");
            $(this).css("border" , "1px solid #1f1f1f");
        }

    });
});


function logout(){
   $.ajax({
      url: baseUrl +"login/logout/local/",
      type: "GET",
      dataType: "json",
      success: function(data){

          if( data.code == "0" ){
              window.location.href = baseUrl;
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}