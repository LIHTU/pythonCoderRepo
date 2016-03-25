$(document).ready(function(){
	$.get("history", function(data, status){
        document.getElementById("history").value = data
    })
})