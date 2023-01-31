$(document).ready(function() {

    $('.summernote').summernote({
        height: 500,
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

    $(document).on("click", ".sendBtn", function(){
       var title = $("#title").val();
       var content = $('.summernote').summernote('code');
       var notView = $("#notView").is(":checked");

       var view = "Y";
       if( notView == true ){
           view = "N";
       }

       if( title == "" ){
           alert("제목을 입력해주세요.");
           return;
       }

       if( content == "" ){
           alert("내용을 입력해주세요.");
           return;
       }

        saveNotice(title, content, view);
    });

    $(document).on("click", ".sendBtn2", function(){
       var title = $("#title").val();
       var content = $('.summernote').summernote('code');
       var notView = $("#notView").is(":checked");

       var view = "Y";
       if( notView == true ){
           view = "N";
       }

       if( title == "" ){
           alert("제목을 입력해주세요.");
           return;
       }

       if( content == "" ){
           alert("내용을 입력해주세요.");
           return;
       }

        editNotice(title, content, view);
    });
});

function uploadSummernoteImageFile(file, editor) {
    data = new FormData();
    data.append("file", file);

    $.ajax({
        data : data,
        type : "POST",
        dataType: "json",
        url : "/onepickAdmin/notice/summerImageUpload/",
        contentType : false,
        processData : false,
        success : function(data) {
            //항상 업로드된 파일의 url이 있어야 한다.
            $(editor).summernote('insertImage', "/media/"+data.url);
        }
    });
}

function saveNotice(title, content, view){
    $.ajax({
      url: "/onepickAdmin/notice/writeCallBack/",
      type : "POST",
      dataType: "json",
      data:{"title":title, "content" : content, "view" : view },
      success: function(data){
         alert("정상적으로 저장되었습니다.");
         window.location.href="/onepickAdmin/notice/list/all/1/";
      },
      error: function (request, status, error){
          alert(error);
      }
   });
}

function editNotice(title, content,view){
    $.ajax({
      url: "/onepickAdmin/notice/editCallBack/",
      type : "POST",
      dataType: "json",
      data:{"num" : num, "title":title, "content" : content, "view" : view },
      success: function(data){
         alert("정상적으로 저장되었습니다.");
         window.location.href="/onepickAdmin/notice/viewer/"+num+"/";
      },
      error: function (request, status, error){
          alert(error);
      }
   });
}