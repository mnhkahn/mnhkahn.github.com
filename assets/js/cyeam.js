$(document).ready(function () {
	// 获取所有 img 标签
	const images = document.getElementsByTagName('img');
	// 遍历 img 标签并添加 onclick 方法
	for (let i = 0; i < images.length; i++) {
		images[i].onclick = function () {
			// alert('你点击了图片');
			var image = images[i];
			image.classList.toggle('enlarged');
		};
	}
});