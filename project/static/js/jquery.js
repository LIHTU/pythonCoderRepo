$(document).ready(function(){
    $("button").click(function(){
        $.post(window.location.protocol + "//" + window.location.host + "/submit",
        {
            text: editor.getValue(),
            dataset: $('#datalist').val()
        },
        function(data, status){
            var table = document.getElementById("assert_table");
            if (data["vals"].length == 0) {
                alert("Code did not run successfully")
            }
            else {
                for (i = 0; i < data["vals"].length; i++) {
                    var cell = table.rows[i].cells[2]
                    var error_cell = table.rows[i].cells[3]
                    if (data["vals"][i][0] == "1") {
                        cell.innerHTML = '&#9989'
                        error_cell.innerHTML = ''
                    }
                    else {
                        cell.innerHTML = "&#10060"
                        error_cell.innerHTML = data["vals"][i][1]
                    }

                }
            }
        })
    })
})
