// 返回顶部悬浮按钮
(function () {
  function init() {
    if (document.getElementById("back-to-top")) return;
    var btn = document.createElement("button");
    btn.id = "back-to-top";
    btn.title = "返回顶部";
    btn.innerHTML = "↑";
    btn.onclick = function () { window.scrollTo({ top: 0, behavior: "smooth" }); };
    document.body.appendChild(btn);
    var toggle = function () {
      btn.classList.toggle("visible", window.scrollY > 400);
    };
    window.addEventListener("scroll", toggle, { passive: true });
    toggle();
  }
  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
