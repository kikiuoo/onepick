$(document).ready(function(){

    $(document).on("click", ".socialBox .socialBtn", function (){
        var loginType = $(this).attr("id");

        // 각 API 구현 필요.
        if( loginType == "kakaoLogin" ){
            window.location.href = baseUrl +"login/kakao/";
        }else if( loginType == "gogleLogin" ){
            window.location.href = baseUrl +"login/google/";
        }else if( loginType == "appleLogin" ){
           // window.location.href = baseUrl +"login/apple/";
        }else if( loginType == "naverLogin" ){
            window.location.href = baseUrl +"login/naver/";
        }
    });

    $(document).on("click", ".joinInfo span", function (){
        window.location.href = baseUrl +"login/joinAgreement_c/";
    });

});