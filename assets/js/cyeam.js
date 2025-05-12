$(document).ready(function () {
	// 获取所有 img 标签
	const images = document.getElementsByTagName('img');
	// 遍历 img 标签并添加 onclick 方法
	for (let i = 0; i < images.length; i++) {
		images[i].onclick = function () {
			var image = images[i];
			showModal(image);
		};
	}
});

function showModal(image) {
	var modal = document.getElementById("modal");
	var modalImage = document.getElementById("modal-image");
	modal.style.display = "block";
	modalImage.src = image.src;
}

function hideModal() {
	var modal = document.getElementById("modal");
	modal.style.display = "none";
}