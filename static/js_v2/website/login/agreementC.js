$(document).ready(function(){

    $(document).on("change", ".textCheck", function(){
        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
            $(this).children("span").css("background-image", 'url("/static/image/web_v2/tick-square_on.png")');
            $(this).children("input").attr("checked","true");;
        }else{
            $(this).css("color", "#595959");
            $(this).children("span").css("background-image", 'url("/static/image/web_v2/tick-square_off.png")');
            $(this).children("input").removeAttr("checked");;
        }
    });


    $(document).on("click", ".allCheck", function(){
        var checked = $(this).children().is(":checked");

        if( checked == true ){
            $(this).css("color", "#ff8aae");
            $(this).children("span").css("background-image", 'url("/static/image/web_v2/tick-square_on.png")');
            $(this).children("input").attr("checked","true");
        }else{
            $(this).css("color", "#595959");
            $(this).children("span").css("background-image", 'url("/static/image/web_v2/tick-square_off.png")');
            $(this).children("input").removeAttr("checked");;
        }

        if( checked == true ){
            $("#agree1,#agree2,#agree3").attr("checked","true");
            $("#agree1,#agree2,#agree3").parents(".textCheck").css("color", "#ff8aae");
            $("#agree1,#agree2,#agree3").parents(".textCheck").children("span").css("background-image", 'url("/static/image/web_v2/tick-square_on.png")');
        }else{
            $("#agree1,#agree2,#agree3").removeAttr("checked","true");
            $("#agree1,#agree2,#agree3").parents(".textCheck").css("color", "#595959");
            $("#agree1,#agree2,#agree3").parents(".textCheck").children("span").css("background-image", 'url("/static/image/web_v2/tick-square_off.png")');
        }
    });


    $(document).on("click", ".joinBtn", function (){
        var agree1 = $("#agree1").is(":checked");
        var agree2 = $("#agree2").is(":checked");
        var agree3 = $("#agree3").is(":checked");

        if( agree1 == false ||  agree3 == false ||  agree2 == false ){
            alert("약관을 확인하고 동의해주세요.");
            return;
        }

        window.location.href = baseUrl +"login/joinCompany/";
    });

    $(document).on("click", ".joinBtn", function (){
        var agree1 = $("#agree1").is(":checked");
        var agree2 = $("#agree2").is(":checked");
        var agree3 = $("#agree3").is(":checked");

        if( agree1 == false ||  agree3 == false ||  agree2 == false ){
            alert("약관을 확인하고 동의해주세요.");
            return;
        }

        window.location.href = baseUrl +"login/joinCompany/";
    });

    $(document).on("click", ".joinBtn2", function (){
        var agree1 = $("#agree1").is(":checked");
        var agree2 = $("#agree2").is(":checked");
        var agree3 = $("#agree3").is(":checked");
        var userID = $("#userID").val();

        if( agree1 == false ||  agree3 == false ||  agree2 == false ){
            alert("약관을 확인하고 동의해주세요.");
            return;
        }

        window.location.href = baseUrl +"login/joinSocial/"+userID+"/";
    });

});