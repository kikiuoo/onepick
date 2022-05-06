$(document).ready(function(){

    $(document).on("change", "#cateMain", function(){

        var cate = $(this).find("option:selected").val();

        getSubCate(cate);

    })


    $(document).on("click", ".ordinaryBtn", function(){

        var disabled = $("#startDate").attr("disabled");

        alert(readOnly);

        if( readOnly == false || readOnly == undefined){
             $("#startDate").prop("disabled", true);
        }else{

        }

    });


     $( "#startDate, #endDate, #auditionDate" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat : 'yy-mm-dd'
    });

    $.datepicker.regional[ "kr" ];


     $("#auditionTime").timepicker({
        timeFormat: 'HH:mm:ss',
        // year, month, day and seconds are not important
        minTime: new Date(0, 0, 0, 0, 0, 0),
        maxTime: new Date(0, 0, 0, 23, 50, 0),
        // time entries start being generated at 6AM but the plugin
        // shows only those within the [minTime, maxTime] interval
        startHour: 6,
        // the value of the first item in the dropdown, when the input
        // field is empty. This overrides the startHour and startMinute
        // options
        startTime: new Date(0, 0, 0, 0, 0, 0),
        // items in the dropdown are separated by at interval minutes
        interval: 10
    });

});

function getSubCate(cate){
    $.ajax({
      url: "/audi/ajax/getSubCate/",
      type: "GET",
      dataType: "html",
      data:{"cate" : cate},

      success: function(data){
          $(".subCateBox").empty().append(data);
      },
      error: function (request, status, error){

      }
   });
}