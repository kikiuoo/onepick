$(document).ready(function(){
    $(document).on("click", ".sendBtn", function (){

        var nowPW = $("#nowPW").val();
        var pw1 = $("#pw1").val();
        var pw2 = $("#pw2").val();

        if( nowPW == "" ){
            alert("기존 패스워드를 입력해주세요.");
            return;
        }

        if( pw1 == "" ){
            alert("패스워드를 입력해주세요.");
            return;
        }

        if( pw2 == "" ){
            alert("패스워드를 입력해주세요.");
            return;
        }

        if( pw1 != pw2 ){
            alert("패스워드와 패스워드 확인이 다릅니다.");
            return;
        }

        savePW(nowPW, pw1);
    });

});


function savePW(nowPW, pw1){
   $.ajax({
      url:  baseUrl + "users/ajax/updatePWCallback/",
      type: "GET",
      dataType: "json",
      data:{"nowPW" : nowPW,"pw1" : pw1},

      success: function(data){

          if( data.code == "0" ){
             alert("패스워드 변경이 완료되었습니다.")
             window.history.back();
          }else{
              alert( data.message );
          }
      },
      error: function (request, status, error){

      }
   });
}