$(document).ready(readyFunction);

function readyFunction(){
    checkbox = document.getElementById("newoption");
    checkbox.onchange = function() {
        if(checkbox.checked) {
            $(".newname").show();
        }
    }
    $("button.newname").on('click', function() {
        var newHeading = $("input#newname").val();
        var newPriority = $("input#newpriority").val();
        console.log(newHeading);
        console.log(newPriority);
        var newData = '{"heading":"' + newHeading + '", "priority":"' + parseInt(newPriority) + '"}';
        console.log(newData);
        var JsonNewData = JSON.parse(newData);
        $.ajax({
            type: "POST",
            url: $SCRIPT_ROOT + '/new',
            processData: false,
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            data: JSON.stringify(JsonNewData, null, '\t'),
            success: function(data) {
                console.log("DataReceived!");
                $("datalist#heading").append('<option value="' + data['priority'] + '">' + data['heading'] + '</option>')
            },
            error: function(jqxhr, status, message) {
                console.log("Error : " + message);
            }
        });
    });
}
