function initArticleTools() {
    initResponsiveTables();
    initImagePreview();
    // 高亮和复制是一组能力：任一基础脚本未就绪时，两者都不初始化，
    // 避免出现只有复制按钮、却没有对应高亮的半完成状态。
    if (initCode()) {
        initCopyBtn();
    }
}

// This deferred local script can initialize before unrelated CDN scripts finish.
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initArticleTools, { once: true });
} else {
    initArticleTools();
}

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
    if (!window.Prism || typeof window.Prism.highlightAll !== "function") {
        console.error("Prism 未加载，代码高亮与复制按钮均不会初始化。");
        return false;
    }
    if (window.Prism.plugins && window.Prism.plugins.Autoloader) {
        window.Prism.plugins.Autoloader.languages_path = "/assets/vendor/prism/components/";
    }
    window.Prism.highlightAll();
    return true;
}

function initCopyBtn() {
    const pres = document.querySelectorAll("pre");
    pres.forEach(function (pre) {
        const codeEl = pre.querySelector("code");
        if (!codeEl) return;

        // The button belongs to the outer frame, not the scrolling pre.
        let frame = pre.parentElement;
        if (!frame.classList.contains("code-block")) {
            frame = document.createElement("div");
            frame.className = "code-block";
            pre.before(frame);
            frame.appendChild(pre);
        }
        pre.classList.remove("position-relative", "my-3");
        pre.classList.add("rounded");
        frame.querySelectorAll(".copy-btn").forEach(function (button) {
            button.remove();
        });

        // 创建复制按钮
        const copyBtn = document.createElement("button");
        copyBtn.className = "copy-btn btn btn-sm btn-outline-secondary";
        copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
        copyBtn.title = "复制代码";
        copyBtn.setAttribute("aria-label", "复制代码");

        // 绑定复制事件
        copyBtn.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            copyToClipboard(codeEl.textContent, copyBtn);
        });

        frame.appendChild(copyBtn);
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

function initResponsiveTables() {
    document.querySelectorAll(".content table").forEach(function (table) {
        if (table.closest(".table-scroll")) return;
        const wrapper = document.createElement("div");
        wrapper.className = "table-scroll";
        wrapper.tabIndex = 0;
        wrapper.setAttribute("role", "region");
        wrapper.setAttribute("aria-label", "表格，可左右滑动查看");
        table.before(wrapper);
        wrapper.appendChild(table);
    });
}

let previewTrigger = null;

function initImagePreview() {
    // Event delegation also covers Mermaid SVGs rendered after page load.
    document.addEventListener("click", function (event) {
        const element = event.target.closest(".content img, .content svg");
        if (!element || element.closest("a, button, .image-preview")) return;
        showModal(element);
    });
    document.addEventListener("keydown", function (event) {
        const modal = document.getElementById("image-preview");
        if (!modal || !modal.classList.contains("is-open")) return;
        if (event.key === "Escape") hideModal();
        if (event.key === "Tab") {
            event.preventDefault();
            modal.querySelector("button").focus();
        }
    });
}

function showModal(element) {
    let modal = document.getElementById("image-preview");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "image-preview";
        modal.className = "image-preview";
        modal.setAttribute("role", "dialog");
        modal.setAttribute("aria-modal", "true");
        modal.setAttribute("aria-label", "图片预览");
        modal.innerHTML = '<button type="button" class="preview-close" aria-label="关闭预览">×</button><img class="modal-image" alt="大图预览" />';
        document.body.appendChild(modal);
        modal.addEventListener("click", function (event) {
            if (event.target === modal || event.target.closest(".preview-close")) hideModal();
        });
    }
    const image = modal.querySelector("img");
    if (element.tagName.toLowerCase() === "svg") {
        const svg = element.cloneNode(true);
        svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        image.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(new XMLSerializer().serializeToString(svg));
    } else {
        image.src = element.currentSrc || element.src;
    }
    image.alt = element.getAttribute("alt") || "图表预览";
    previewTrigger = document.activeElement;
    modal.classList.add("is-open");
    modal.querySelector("button").focus();
}

function hideModal() {
    const modal = document.getElementById("image-preview");
    if (!modal) return;
    modal.classList.remove("is-open");
    modal.querySelector("img").removeAttribute("src");
    if (previewTrigger && previewTrigger.isConnected) previewTrigger.focus();
}
