$(document).ready(function(){	
	window.onunload = function() {
		Cookies.set("code", editor.getValue());

	}
})