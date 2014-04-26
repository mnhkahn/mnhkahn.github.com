function doodle() {
	alert("mobile")
	$.getJSON("http://doodle.cyeam.com/js?jsoncallback=?", function(json) {
		$("body").css("background", "url(" + json[0].doodle + ") center no-repeat fixed");
	});
}

function getDoodle(doodle_container, title_container) {
	$.getJSON("http://doodle.cyeam.com/js?jsoncallback=?", function(json) {
		document.getElementById(doodle_container).src = json[0].doodle;
		document.getElementById(title_container).innerHTML = json[0].title;
		// $("#" + container).css("src", json[0].doodle);
	});
}

function bing(container) {
	alert("pc")
	if (container != null) {
		$.getJSON("http://bing.cyeam.com/js?jsoncallback=?", function(json) {
			$("#" + container).css("background", "url(" + json[0].bing + ") no-repeat center center");
		});
	} else {
		$.getJSON("http://bing.cyeam.com/js?jsoncallback=?", function(json) {
			$("body").css("background", "url(" + json[0].bing + ") no-repeat center center fixed");
		});
	}
}

function wallpaper() {
	$.getJSON("http://lab.cyeam.com/api/ip?jsoncallback=?", function (json) {
    if (json[0].useragent.IsMobile == "true") {
        doodle()
    } else {
        bing()
    }
});
}