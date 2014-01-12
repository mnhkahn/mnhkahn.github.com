/* Introduction
Parameters:
[container]: needs a container to hold this slide window;
[size]: slide windows' length and width;
[arr]: slide window's picture and describe message.
{{link:'/image/1.jpg',desc:'one'}, {link:'/image/2.jpg',desc:'two'}, {link:'/image/3.jpg',desc:'three'}, {link:'/image/4.jpg',desc:'four'}}
*/
var cSlide = {
	create: function(containerID, size, arr) {
		this.margin_left = 10;
		this.margin_top = 10;
		this.container = $('#' + containerID);
		this.size = size;
		this.arr = arr.windows;
		this.position = new Array();
		
		this._showSlide(this.container, this.size, this.arr);
	},
	
	_showSlide: function(container, size, arr) {
		var THIS = this;
	
		// set container's style sheet
		container.css("position", "relative");
		container.css("overflow", "hidden");
		container.css("width", size.width);
		container.css("height", size.height);
		container.css("border", "1px solid #ededed");
		
		// left arrow		
		var leftArrow = $('<div></div>');
		leftArrow.addClass("leftArrow");
		leftArrow.attr("id", "leftArrow");
		leftArrow.css("position", "absolute");
		leftArrow.css("width", "23px")
		leftArrow.css("height", "46px");
		leftArrow.css("left", "0");
		leftArrow.css("top", (this.container.height() - leftArrow.height()) / 2);
		leftArrow.css("z-index", "5");
		leftArrow.css("background-image", "url(/images/arrowLeft.png)");
		leftArrow.click(function(){THIS.move(true, 10, 0)});

		container.append(leftArrow);
		
		// slide wrapper
		var slideWrapper = $('<div></div>');
		slideWrapper.addClass("slideWrapper");
		var slideWrapper = $('<div></div>');
		slideWrapper.addClass("slideWrapper");
		slideWrapper.attr('id', "slideWrapper" + container);
		slideWrapper.css("position", "relative");
		slideWrapper.css("width", container.width() - THIS.margin_left * 2);
		slideWrapper.css("height", container.height() - THIS.margin_top * 2);
		slideWrapper.css("margin", "0 auto");
		slideWrapper.css("overflow", "hidden");
		slideWrapper.css("margin-left", THIS.margin_left);
		slideWrapper.css("margin-top", THIS.margin_top);
		slideWrapper.css("-webkit-box-shadow", "0 2px 4px rgba(0,0,0,0.2)");
		
		slideWrapper.hover(
			function() {
				THIS.stopMove();
			},
			function() {
				THIS.startMove();
			}
		);
		
		var lastPos = 0 - size.width;
		for(i in arr) {
			this.position[i] = lastPos + size.width;
			lastPos = this.position[i];
		}
		for(i in arr) {
			var Windows = $("<div></div>");
			Windows.addClass("Windows");
			Windows.css("overflow", "hidden");
			Windows.css("position", "absolute");
			Windows.css("width", slideWrapper.width());
			Windows.css("height", slideWrapper.height());
			Windows.css("left", this.position[i]);
			Windows.attr("id", "Windows" + i);
			Windows.html("<img class='slideImg' style='overflow:hidden;' src='" + arr[i].pic + "'></img>");

			var Messages = $("<div></div>");
			Messages.addClass("Message");
			Messages.css("width", slideWrapper.width());
			Messages.css("height", 70);
			Messages.css("z-index", "5");
			Messages.css("position", "absolute");
			Messages.css("bottom", 0);
			Messages.css("background-color", "rgb(237,237,237)");
			Messages.css("filter", "alpha(opacity:90)");
			Messages.css("opacity", 0.9);
			Messages.attr("id", "Message" + i);
			Messages.css("display", "none");

			// Open new tab
			Messages.css("cursor", "hand");
			Messages.click(function(event){
				var i = event.currentTarget.id.substring(7);
				THIS.hiddenMessage(event);
				window.open(arr[i].link, 'newwindow')
			});

			var MessageDesc = $("<p></p>");
			MessageDesc.addClass("MessageTitle");
			MessageDesc.css("width", slideWrapper.width() - 30);
			MessageDesc.css("height", 30);
			MessageDesc.css("padding-left", 15);
			MessageDesc.html(arr[i].desc);
			Messages.append(MessageDesc);
			

			Windows.append(Messages);

			Windows.hover(
				function(event) {
					THIS.showMessage(event);
				},
				function(event) {
					THIS.hiddenMessage(event);
				}
			);

			slideWrapper.append(Windows);
		}
		
		container.append(slideWrapper);
		
		// right arrow
		var rightArrow = $('<div></div>');
		rightArrow.addClass("rightArrow");
		rightArrow.attr("id", "rightArrow");
		rightArrow.css("position", "absolute");
		rightArrow.css("width", "23px")
		rightArrow.css("height", "46px");
		rightArrow.css("right", 0);
		rightArrow.css("top", (this.container.height() - rightArrow.height()) / 2);
		rightArrow.css("z-index", "5");
		rightArrow.css("background-image", "url(/images/arrowRight.png)");
		rightArrow.click(function(){THIS.move(false, 10, 0)});

		container.append(rightArrow);
		
		// slide action by timer
		THIS.startMove();
	},
	
	// isPrevious: true move previously, false move next
	move: function(isPrevious, steps, times) {
		var THIS = this;
		window.setTimeout(
			function() {
				times++;
				for (i in THIS.position) {
					var flagPrevious = isPrevious ? 1 : -1;
					THIS.position[i] += flagPrevious * THIS.size.width / steps;
					$('#Windows' + i).css("left", THIS.position[i]);
				}

				// reset position
				for (i in THIS.position) {
					if (THIS.position[i] <= -(THIS.position.length - 1) * THIS.size.width) {
						THIS.position[i] += THIS.position.length * THIS.size.width;
					}
					if (THIS.position[i] >= (THIS.position.length - 1) * THIS.size.width) {
						THIS.position[i] -= THIS.position.length * THIS.size.width;
					}
				}

				if (times < steps) {
					THIS.move(isPrevious, steps, times);
				}
			},
			50
		);
		//	console.debug(position);
	},
	
	startMove: function() {
		var THIS = this;
		THIS.changeTimer = window.setInterval(function(){THIS.move(false, 10, 0)}, 5000);
	},

	stopMove: function() {
		if (this.changeTimer) {
			window.clearInterval(this.changeTimer);
		}
	},

	showMessage: function(event) {
		var index = event.currentTarget.id.substring(7);
//		console.debug(index);
		$('#Message' + index).fadeIn("slow");
	},

	hiddenMessage: function(event) {
		var index = event.currentTarget.id.substring(7);
//		console.debug(index);
		$('#Message' + index).fadeOut("slow");
	}
}
