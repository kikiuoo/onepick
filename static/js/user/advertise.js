$(document).ready(function(){

    $(document).on("click", ".sendBtn", function(){

        var email = $("#email").val();
        var title = $("#title").val();
        var content = $("#content").val();

        if( email == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        if( title == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        if( content == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        saveAdvertise(email, title, content);
    });

    $(document).on("click", ".sendBtn2", function(){

        var cate = $("#cate").find(":selected").val();
        var title = $("#title").val();
        var content = $("#content").val();

        if( cate == "" ){
            alert("카테고리를 선택해 주세요.");
            return;
        }

        if( title == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        if( content == "" ){
            alert("이메일을 입력해 주세요.");
            return;
        }

        $("#saveQanda").submit();
    });


    // 기본정보 선택시 글자 색상 변경
    $(document).on("change", "select", function(){
        $(this).css("color", "#1f1f1f");
    });

    $(document).on("change", ".textCheck", function(){
        var checked = $(this).children().is(":checked");

        if (checked == true) {
            $(this).css("color", "#ff8aae");
            $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_on.png")');
            $(this).children("input").attr("checked", "true");
        }else{
            $(this).css("color", "#c0c0c0");
            $(this).children("div").css("background-image", 'url("/static/image/web/textCheck_off.png")');
            $(this).children("input").removeAttr("checked", "true");
        }

    });

});


function saveAdvertise(email, title, content){
   $.ajax({
      url: "/advertise/callBack/",
      type: "GET",
      dataType: "json",
      data:{"email" : email, "title" : title, "content" : content},

      success: function(data){

          if( data.code == "0" ){
              alert("정상적으로 접수되었습니다.")
              window.location.replace("/advertise/");
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}
