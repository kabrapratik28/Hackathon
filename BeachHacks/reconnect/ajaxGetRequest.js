$(document).ready(function() {
    console.log('ready');

var colors = ["success","info","warning","danger"]
var leng_colors = colors.length;
var run_counter = 0;

//Submit Button Function
var submit = function(event) {
    event.preventDefault();


    //create an empty obj, list prop, and store val
    var user_name =  $("#user_name").val();

    var urlAjax =  "http://127.0.0.1:5000/time/"+user_name ;

    var jqxhr = $.ajax({
        type: "GET",
        url: urlAjax,
        //contentType: "application/json",
        success: function(data) { console.log(data);
        table_data = `<table class="table">
        <thead>
            <tr>
                <th>Timing Slots</th>
                <th>Friends Available</th>
            </tr>
       </thead>`;

            var timing_data = data.timing;
            for (i = 0; i < timing_data.length; i++) { 
                each_row = "<tr class="+ colors[run_counter] +"> <td> " + timing_data[i][1] + "</td> <td> " + timing_data[i][0] + "</td> </tr>"; 
                run_counter = run_counter + 1;
                run_counter = run_counter % leng_colors;
                table_data += each_row;
            }
        
        table_data = table_data + "</table>";
            $(".result").html(`
            <div class="page-header">
              <h1>Connect Timings!</h1>      
            </div>`
             + "<br>"+table_data);
        
        },
        error: function(data) {alert("ajax error"); },
        dataType: 'json'
    });


    console.log("data got!");


    };
    $("#submit").on("click", submit);



//Add Input Button, i.e.
   

//end of add input field

});