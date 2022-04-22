$(document).ready(function(){

    // 메인 베너 클릭 이벤트

    // 전체보기 클릭 이벤트
    $(document).on("click", ".title span" ,function(){
        var url = $(this).attr("data-url");

        window.location.href = url;
    });

    // viewer 선택.
    $(document).on("click", ".audition", function(){
       var num = $(this).attr("data-num");

       window.location.href = '/audi/audiDetail/'+cateType+'/' +num +"/";
    });
    
    $(document).on("click", ".pickBtn", function(){
       // pick 기능 추가 구현 필요
    });

});