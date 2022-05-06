$(document).ready(function(){

    $(document).on("change", "#email_select", function (){
        var data = $("#email_select").find("option:selected").val();
        $("#email2").val(data);
    });

    $(document).on("click", "#allCheck", function (){

        var check = $("#allCheck").is(":checked");

        if( check == true ){
            $(".agree").prop('checked', true);
        }else if( check == false ){
            $(".agree").prop('checked', false);
        }

    });

    $(document).on("click", ".sendBtn", function (){

        var name = $("#name").val();
        var phone2 = $("#phone2").val();
        var phone3 = $("#phone3").val();
        var email11 = $("#email11").val();
        var email12 = $("#email12").val();
        var brith1 = $("#brith1").val();
        var brith2 = $("#brith2").val();
        var brith3 = $("#brith3").val();

        if( name == "" ){
            alert("이름을 입력해주세요.");
            return;
        }

        if( phone2 == "" || phone3 == "" ){
            alert("전화번호를 정확히 입력해주세요.");
            return;
        }
        
        if( email11 == "" || email12 == "" ){
            alert("이메일을 정확히 입력해주세요.");
            return;
        }
        
        if( brith1 == "" || brith2 == "" || brith3 == "" ){
            alert("생년월일을 정확히 입력해주세요.");
            return;
        }
        
        if ($('.agree:checked').length != $('.agree').length) {
            alert("약관에 모두 동의해주세요.");
            return;
        }

        $("#saveUserForm").submit();
    });

});

