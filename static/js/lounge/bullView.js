$(document).ready(function(){
     $(document).on("click", ".saveComment", function (){

        if( userID == "" ){
            alert("로그인 후 이용 가능합니다.");
            return;
        }

        var comment = $("#comment").val();

        if( comment == "" ){
            alert("댓글 내용을 입력해주세요.");
            return;
        }

        $("#comment").val("");
        saveComment(comment);
    });


    $(document).on("keyup", "#comment", function (e){
        if(e.keyCode==13) {
            $(".saveComment").trigger("click");
        }
    });


    $(document).on("click", ".commentDelete", function (){
       var num = $(this).attr("data-num");

       if(confirm("댓글을 삭제하시겠습니까?") == true){
           deleteComment(num);
       }
    });


    $(document).on("click", ".editBtn", function (){
       var num = $(this).attr("data-num");

       window.location.href = "/lounge/bull/edit/"+num+"/";
    });


    $(document).on("click", ".delBtn", function (){
       var num = $(this).attr("data-num");

       window.location.href = "/lounge/bull/delete/"+num+"/";
    });


});


function saveComment(comment){
    $.ajax({
      url: "/lounge/bull/ajax/saveComment/",
      type: "GET",
      dataType: "json",
      data:{"comment" : comment, "num" : num},

      success: function(data){
          if( data.code == "0"){
            reloadComment();
          }
      }
      ,
      error: function (request, status, error){

      }

   });
}

function reloadComment(){
    $.ajax({
      url: "/lounge/bull/ajax/reloadComment/",
      type: "GET",
      dataType: "html",
      data:{ "num" : num},

      success: function(data){
          $(".commentList").empty().append(data);
      }
      ,
      error: function (request, status, error){

      }

   });
}

function deleteComment(num){
    $.ajax({
      url: "/lounge/bull/ajax/deleteComment/",
      type: "GET",
      dataType: "json",
      data:{ "num" : num },

      success: function(data){
          if( data.code == "0"){
            reloadComment();
          }
      }
      ,
      error: function (request, status, error){

      }

   });
}