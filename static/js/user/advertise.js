$(document).ready(function(){

    $(document).on("click", ".sendBtn", function(){

        var email = $("#email").val();
        var title = $("#title").val();
        var content = $("#content").val();

        alert(content);

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

});


function saveAdvertise(email, title, content){
   $.ajax({
      url: "/advertise/callBack/",
      type: "POST",
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
