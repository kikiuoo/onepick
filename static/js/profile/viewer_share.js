$(document).ready(function(){

     if( isDelete == '1'){
        alert("잘못된 접근입니다.");
        window.history.back(-1);
    }

    $(".allImage").text(imageCount);

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
