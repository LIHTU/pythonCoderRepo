$(document).ready(function(){
    console.log()
    $("button").click(function(){

        $.post(window.location.protocol + "//" + window.location.host + "/submit",
        {
            text: $('#code').val(),
            dataset: $('#datalist').val()
        },
        function(data, status){
            if (data == "Success") {
                $("#x").hide();
                $("#x1").hide();
                $("#x2").hide();
                $("#check").show()
                $("#check1").show()
                $("#check2").show()
            }
        });
    });
});