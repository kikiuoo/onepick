$(document).ready(function (){
    // 메인 베너 클릭 이벤트
    $(document).on("click", ".mainBanner", function (){
        // 추가 개발.
    });

    // Title 전체보기 클릭 이벤트 (Web 만 사용)
    $(document).on("click", ".mainTitle span", function(){
        var url = $(this).attr("data-url");

        window.location.href = url;
    });

    // 오디션 클릭 이벤트
    $(document).on("click", ".audition", function(){
       var num = $(this).attr("data-num");

       window.location.href = "/audi/audiDetail/actor/" + num + "/" //  ../audi/audiDetail/actor(기본값)/글번호/
    });

    // 오디션 픽 기능. ( 구현 필요 )
    $(document).on("click", ".audition .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        // 기능 구현 필요
    });

    // 프로필 클릭 이벤트
    $(document).on("click", ".profile", function(){
       var num = $(this).attr("data-num");

       window.location.href = "/profile/profDetail/" + num + "/" //  ../profile/profDetail/글번호/
    });

    // 프로필 픽 기능. ( 구현 필요 )
    $(document).on("click", ".profile .pickBtn", function(e){
        e.preventDefault();
        e.stopPropagation();

        // 기능 구현 필요
    });

    // 소베너 클릭이벤트
    $(document).on("click", ".subBanner", function(){
       var url = $(this).attr("data-url");

       window.location.href = url;
    });
});