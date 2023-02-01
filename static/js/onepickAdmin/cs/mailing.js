$(document).ready(function() {

    $('.summernote').summernote({
        height: 450,
        lang: "ko-KR",					// 한글 설정
        callbacks: {	//여기 부분이 이미지를 첨부하는 부분
					onImageUpload : function(files) {
						uploadSummernoteImageFile(files[0],this);
					},
					onPaste: function (e) {
						var clipboardData = e.originalEvent.clipboardData;
						if (clipboardData && clipboardData.items && clipboardData.items.length) {
							var item = clipboardData.items[0];
							if (item.kind === 'file' && item.type.indexOf('image/') !== -1) {
								e.preventDefault();
							}
						}
					}
				},
        toolbar: [
			    // [groupName, [list of button]]
			    ['fontname', ['fontname']],
			    ['fontsize', ['fontsize']],
			    ['style', ['bold', 'italic', 'underline','strikethrough', 'clear']],
			    ['color', ['forecolor','color']],
			    ['table', ['table']],
			    ['para', ['ul', 'ol', 'paragraph']],
			    ['height', ['height']],
			    ['insert',['picture','link','video']]
			  ],
			fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New','맑은 고딕','궁서','굴림체','굴림','돋움체','바탕체'],
			fontSizes: ['8','9','10','11','12','14','16','18','20','22','24','28','30','36','50','72']
    });

    $(document).on("change", "#userType, #geneder", function(){
        var index = $(this).find("option:selected").index();

        if( index == 0 ){
            $(this).css("color", "#c0c0c0");
        }else{
            $(this).css("color", "#1f1f1f");
        }

        var userType = $("#userType").find("option:selected").val();
        var geneder = $("#geneder").find("option:selected").val();
        var age1 = $("#age1").val();
        var age2 = $("#age2").val();
        var name = $("#name").val();

        getUserList( userType, geneder, age1, age2, name);
    });

    $(document).on("keyup", "#age1, #age2, #name, #height1, #height2", function(){
        var userType = $("#userType").find("option:selected").val();
        var geneder = $("#geneder").find("option:selected").val();
        var age1 = $("#age1").val();
        var age2 = $("#age2").val();
        var name = $("#name").val();

        getUserList( userType, geneder, age1, age2, name);
    });

    $(document).on("change", ".profileCheck", function (){
       var selectUser = $(".profileCheck:checked").length;

       $("#selCount").text(selectUser);
    });

    $("#allCheck").click(function() {
        if($("#allCheck").is(":checked")){
            $(".profileCheck").prop("checked", true);

            var allCount = $("#allCount").text();
            $("#selCount").text(allCount);
        }
        else{
            $(".profileCheck").prop("checked", false);
            $("#selCount").text("0");
        }
    });

    $(document).on("click", ".sendBtn", function(){
       var title = $("#title").val();
       var content = $('.summernote').summernote('code');
       var selectUser = $(".profileCheck:checked").length;

       if( title == "" ){
           alert("제목을 입력해주세요.");
           return;
       }

       if( content == "" ){
           alert("내용을 입력해주세요.");
           return;
       }

       if( selectUser == 0 ){
           alert("수신자를 선택해주세요.");
           return;
       }

       const arr = [];
        // 체크한 항목만 취득
        var user = $("input[name='profile']:checked");
        $(user).each(function() {
            arr.push($(this).val());
        });

        var sendList = arr.join(",");

        sendMail(title, content, sendList);
    });

});


function getUserList(userType, geneder, age1, age2, name){
    $.ajax({
      url: "/onepickAdmin/cs/ajaxUserList/",
      type: "GET",
      dataType: "html",
      data:{"userType":userType, "geneder" : geneder,"age1" : age1, "age2" : age2, "name":name },

      success: function(data){
          $(".contentBox").empty().append(data);

          var userCount = $("#userCount").text();
          $("#allCount").text(userCount);
          $("#selCount").text("0");
      },
      error: function (request, status, error){
          alert(error);
      }
   });
}



function uploadSummernoteImageFile(file, editor) {
    data = new FormData();
    data.append("file", file);

    $.ajax({
        data : data,
        type : "POST",
        dataType: "json",
        url : "/onepickAdmin/cs/summerImageUpload/",
        contentType : false,
        processData : false,
        success : function(data) {
            //항상 업로드된 파일의 url이 있어야 한다.
            $(editor).summernote('insertImage', "https://myonepick.com/media/"+data.url);
        }
    });
}

function sendMail(title, content, sendList){
    $.ajax({
      url: "/onepickAdmin/cs/sendMail/",
      type : "POST",
      dataType: "json",
      data:{"title":title, "content" : content,"sendList" : sendList },
      success: function(data){
         alert("전송이 완료되었습니다.");
         window.location.reload();
      },
      error: function (request, status, error){
          alert(error);
      }
   });
}