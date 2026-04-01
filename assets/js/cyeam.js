$(document).ready(function () {
    initImagePreview();
    initCode();
    initCopyBtn();
});

function initCode() {
    const codeBlocks = document.querySelectorAll("code");
    codeBlocks.forEach(function (codeEl) {
        // 4. 给 <code> 补充默认语言类（如果没有的话）
        if (!codeEl.className.includes("language-")) {
            codeEl.className = "language-text"; // 默认设为纯文本
        } else {
            codeEl.className += ""; // 已有语言类，只加内边距
        }
    });
    Prism.highlightAll();
}

function initCopyBtn() {
    const pres = document.querySelectorAll("pre");
    pres.forEach(function (pre) {
        // 【关键修复】确保 <pre> 有 position-relative，作为按钮的定位参照
        pre.classList.add("position-relative", "rounded", "my-3");

        // 查找 <pre> 里的 <code>
        const codeEl = pre.querySelector("code");
        if (!codeEl) return;

        // 如果按钮已经存在，先删掉（避免重复添加）
        const existingBtn = pre.querySelector(".copy-btn");
        if (existingBtn) existingBtn.remove();

        // 创建复制按钮
        const copyBtn = document.createElement("button");
        copyBtn.className = "copy-btn btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2 z-1";
        copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
        copyBtn.title = "复制代码";
        copyBtn.style.zIndex = "10"; // 确保按钮在代码之上

        // 绑定复制事件
        copyBtn.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            copyToClipboard(codeEl.textContent, copyBtn);
        });

        // 将按钮插入到 <pre> 的末尾
        pre.appendChild(copyBtn);
    });
}

function copyToClipboard(text, btn) {
    navigator.clipboard
        .writeText(text)
        .then(function () {
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="bi bi-check-circle"></i>已复制';
            btn.classList.remove("btn-outline-secondary");
            btn.classList.add("btn-success");
            setTimeout(function () {
                btn.innerHTML = originalText;
                btn.classList.remove("btn-success");
                btn.classList.add("btn-outline-secondary");
            }, 2000);
        })
        .catch(function (err) {
            console.error("复制失败:", err);
            btn.innerHTML = "复制失败";
            setTimeout(function () {
                btn.innerHTML = '<i class="bi bi-clipboard"></i>';
            }, 2000);
        });
}

function initImagePreview() {
    // 同时获取所有 img 和 svg 标签（使用 querySelectorAll 支持多选择器）
    const elements = document.querySelectorAll("img, svg");
    // 遍历元素并为每个元素绑定点击事件
    elements.forEach(function (element) {
        element.onclick = function () {
            // 直接传入当前点击的元素（避免循环变量闭包问题）
            showModal(element);
        };
    });
}
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
