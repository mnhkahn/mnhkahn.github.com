function doodle() {
	$.getJSON("http://doodle.cyeam.com/js?jsoncallback=?", function(json) {
		console.debug(json)
		$("body").css("background", "url(" + json[0].doodle + ") center no-repeat fixed");
	});
}