// 顶部阅读进度条
(function () {
  var bar = document.createElement("div");
  bar.id = "reading-progress";
  document.body.appendChild(bar);
  function update() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
    bar.style.width = pct + "%";
  }
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
})();

// 时间线超过 6 条自动折叠
(function () {
  function fold() {
    var ul = document.getElementById("home-timeline");
    if (!ul || ul.dataset.folded === "1") return;
    var items = ul.querySelectorAll(":scope > li");
    if (items.length <= 6) return;
    items.forEach(function (li, idx) { if (idx >= 6) li.classList.add("timeline-extra"); });
    var more = document.createElement("span");
    more.id = "timeline-more";
    more.textContent = "▼ 显示更早的 " + (items.length - 6) + " 条";
    more.onclick = function () {
      ul.classList.add("expanded");
      more.remove();
    };
    ul.after(more);
    ul.dataset.folded = "1";
  }
  if (document.readyState !== "loading") fold();
  else document.addEventListener("DOMContentLoaded", fold);
})();
