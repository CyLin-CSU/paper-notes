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

// 时间线默认显示最近 3 条，其余折叠进可键盘操作的按钮
(function () {
  function fold() {
    var ul = document.getElementById("home-timeline");
    if (!ul || ul.dataset.folded === "1") return;
    var items = ul.querySelectorAll(":scope > li");
    var VISIBLE = 3;
    if (items.length <= VISIBLE) return;
    items.forEach(function (li, idx) { if (idx >= VISIBLE) li.classList.add("timeline-extra"); });
    var more = document.createElement("button");
    more.type = "button";
    more.id = "timeline-more";
    more.setAttribute("aria-expanded", "false");
    more.textContent = "▼ 显示更早的 " + (items.length - VISIBLE) + " 条";
    more.addEventListener("click", function () {
      ul.classList.add("expanded");
      more.remove();
    });
    ul.after(more);
    ul.dataset.folded = "1";
  }
  if (document.readyState !== "loading") fold();
  else document.addEventListener("DOMContentLoaded", fold);
})();
