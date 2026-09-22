// Giscus 评论系统（基于 GitHub Discussions，数据存在本仓库）
// ── 首次启用需完成一次性配置 ──
// 1. 仓库 Settings → General → Features → 勾选 Discussions
// 2. 打开 https://giscus.app/zh-CN ，输入仓库名 CyLin-CSU/paper-notes
// 3. 按页面引导安装 giscus App；映射方式选 pathname，分类选 Announcements
// 4. 把页面生成的 data-repo-id 和 data-category-id 填到下面两个引号里
var GISCUS_CONFIG = {
  repo: "CyLin-CSU/paper-notes",
  repoId: "R_kgDOUf1vkQ",
  category: "Announcements",
  categoryId: "DIC_kwDOUf1vkc4DF4aj"
};

function mountGiscus() {
  var container = document.getElementById("giscus-container");
  if (!container || container.dataset.mounted === "1") return;
  if (!GISCUS_CONFIG.repoId || !GISCUS_CONFIG.categoryId) {
    container.innerHTML =
      '<div class="giscus-notconfigured">💬 评论区已就位，等待站主完成 giscus 一次性配置：启用仓库 Discussions → 安装 giscus App → 在 giscus.app 获取并填入 repo-id / category-id。完成前访客看不到输入框。</div>';
    return;
  }
  container.dataset.mounted = "1";
  var s = document.createElement("script");
  s.src = "https://giscus.app/client.js";
  s.setAttribute("data-repo", GISCUS_CONFIG.repo);
  s.setAttribute("data-repo-id", GISCUS_CONFIG.repoId);
  s.setAttribute("data-category", GISCUS_CONFIG.category);
  s.setAttribute("data-category-id", GISCUS_CONFIG.categoryId);
  s.setAttribute("data-mapping", "pathname");
  s.setAttribute("data-strict", "0");
  s.setAttribute("data-reactions-enabled", "1");
  s.setAttribute("data-emit-metadata", "0");
  s.setAttribute("data-input-position", "top");
  s.setAttribute("data-theme", "preferred_color_scheme");
  s.setAttribute("data-lang", "zh-CN");
  s.setAttribute("data-loading", "lazy");
  s.crossOrigin = "anonymous";
  s.async = true;
  container.appendChild(s);
}

if (document.readyState !== "loading") {
  mountGiscus();
} else {
  document.addEventListener("DOMContentLoaded", mountGiscus);
}

// 跟随 Material 明暗切换，同步 giscus 主题
window.addEventListener("load", function () {
  if (!("MutationObserver" in window)) return;
  var observer = new MutationObserver(function () {
    var scheme = document.body.getAttribute("data-md-color-scheme");
    var theme = scheme === "slate" ? "dark" : "light";
    var frame = document.querySelector("iframe.giscus-frame");
    if (frame) {
      frame.contentWindow.postMessage(
        { giscus: { setConfig: { theme: theme } } },
        "https://giscus.app"
      );
    }
  });
  observer.observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
});
