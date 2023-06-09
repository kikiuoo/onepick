$(document).ready(function () {

    $(document).on("click", ".contentList", function () {
        var num = $(this).attr("data-num");

        window.location.href = "/onepickAdmin/user/edit/" + num + "/";
    });

    $(document).on("click", ".leftPage, .pages, .rightPage", function () {
        var page = $(this).attr("data-page");
        var listType = $(this).attr("data-type");

        if (listType == "search") {
            window.location.href = "/onepickAdmin/user/listSearch/" + type + "/" + word + "/" + page + "/";
        } else {
            window.location.href = "/onepickAdmin/user/list/" + type + "/" + page + "/";
        }
    });

    $(document).on("click", ".editBtn", function (e) {
        e.preventDefault();
        e.stopPropagation();

        var num = $(this).attr("data-num");
        window.location.href = "/onepickAdmin/user/edit/" + num + "/";
    });


    $(document).on("click", ".delBtn", function (e) {
        e.preventDefault();
        e.stopPropagation();

        var num = $(this).attr("data-num");

        if (confirm("해당 회원을 탈퇴처리하겠습니까?") == true) {
            window.location.href = "/onepickAdmin/user/delete/"+num+"/";
        }
    });

    $(document).on("click", ".search", function () {
        var searchWord = $("#search").val();

        window.location.href = "/onepickAdmin/user/listSearch/" + type + "/" + searchWord + "/1/";
    });

    $(document).on("click", ".excelBtn", function () {
        window.location.href = "/onepickAdmin/user/excel/" + type + "/" + word + "/";
    });

    // 기업회원 등록하기
    $(document).on("click", ".addBtn", function () {
        var page = $(this).attr("data-page");

        window.location.href = "/onepickAdmin/user/addCompany/";
    });
});
