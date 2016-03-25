function get_hint(code1) {
    $.post(window.location.protocol + "//" + window.location.host + "/get_hint",
    {
            text: code1,
            dataset: document.getElementById('datalist').value
         
    },
    function(data, status){

    	document.getElementById('hints').innerHTML = data
    })

}


$(document).ready(function(){
	$('select').on('change', function() {
	    $.post(window.location.protocol + "//" + window.location.host + "/get_asserts/" + document.getElementById('datalist').value, 
	        function(data, status){
	            _data = JSON.parse(data)
	            var len = _data.length
				$("#assert_table tr").remove(); 
				var table = document.getElementById("assert_table");
	            for (var i = 0; i < len; i++) {
	            	// table.createCaption()
	            	// table.innerHTML = "Assertion Statements"
	            	var row = table.insertRow(-1);
	            	var cell1 = row.insertCell(0);
    				var cell2 = row.insertCell(1);
    				var cell3 = row.insertCell(2);
    				var cell4 = row.insertCell(3);
    				cell2.innerHTML = _data[i];
    				cell3.innerHTML = '&#10060';
    				var button = document.createElement('input');
    				button.setAttribute('type','button');
    				button.setAttribute('row', i)
    				button.setAttribute('value','Hint');
    				button.onclick = function() {
    					$.post(window.location.protocol + "//" + window.location.host + "/get_hint",
    						{
					            text: table.rows[parseInt(this.getAttribute('row'))].cells[1].innerHTML,
					            dataset: document.getElementById('datalist').value
         
    						},
    						function(data, status){
    							document.getElementById('hints').innerHTML = "<h2>Hint</h2><br>" + data
    						})
    				}
    				cell1.appendChild(button)
	            }
	        })
	})
});