$(document).ready(function () {
    // 同时获取所有 img 和 svg 标签（使用 querySelectorAll 支持多选择器）
    const elements = document.querySelectorAll("img, svg");

    // 遍历元素并为每个元素绑定点击事件
    elements.forEach(function (element) {
        element.onclick = function () {
            // 直接传入当前点击的元素（避免循环变量闭包问题）
            showModal(element);
        };
    });
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
