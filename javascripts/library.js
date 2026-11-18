/* 论文库筛选：渐进增强——无脚本时下方完整目录照常可读。
   筛选状态写入 URL 参数（group/type/ymin/ymax/code/doi/q），分享链接可复现。 */
(function () {
  "use strict";
  var list = document.getElementById("library-list");
  if (!list) return;
  var items = Array.prototype.slice.call(list.querySelectorAll(".lib-item"));
  var controls = Array.prototype.slice.call(document.querySelectorAll(".lib-f"));
  var ymin = document.getElementById("lib-ymin");
  var ymax = document.getElementById("lib-ymax");
  var q = document.getElementById("lib-q");
  var count = document.getElementById("lib-count");

  function state() {
    var s = {};
    controls.forEach(function (c) { (s[c.dataset.f] = s[c.dataset.f] || []).push(c.value); });
    s._on = {};
    controls.forEach(function (c) { if (c.checked) (s._on[c.dataset.f] = s._on[c.dataset.f] || []).push(c.value); });
    s.ymin = ymin ? +ymin.value : 0;
    s.ymax = ymax ? +ymax.value : 9999;
    s.q = q ? q.value.trim().toLowerCase() : "";
    return s;
  }

  function apply() {
    var s = state(), shown = 0;
    items.forEach(function (it) {
      var ok = true;
      ["type", "group", "code", "doi"].forEach(function (f) {
        var on = s._on[f];
        if (on && on.length && on.indexOf(it.dataset[f]) === -1) ok = false;
      });
      var y = +it.dataset.year;
      if (ok && y && (y < s.ymin || y > s.ymax)) ok = false;
      if (ok && s.q) {
        var hay = it.textContent.toLowerCase();
        if (hay.indexOf(s.q) === -1) ok = false;
      }
      it.style.display = ok ? "" : "none";
      if (ok) shown++;
    });
    if (count) count.textContent = shown;
    var url = new URL(location.href);
    ["type", "group", "code", "doi"].forEach(function (f) {
      var on = s._on[f];
      var allOn = controls.filter(function (c) { return c.dataset.f === f; }).every(function (c) { return c.checked; });
      if (!on || !on.length || allOn) url.searchParams.delete(f); else url.searchParams.set(f, on.join(","));
    });
    if (s.ymin !== 2023) url.searchParams.set("ymin", s.ymin); else url.searchParams.delete("ymin");
    if (s.ymax !== 2026) url.searchParams.set("ymax", s.ymax); else url.searchParams.delete("ymax");
    if (s.q) url.searchParams.set("q", s.q); else url.searchParams.delete("q");
    try { history.replaceState(null, "", url); } catch (e) {}
  }

  function restore() {
    var p = new URLSearchParams(location.search);
    var seq = ["group", "type"];
    p.get("group") && p.get("group").split(",").forEach(function (v) {
      var c = controls.filter(function (x) { return x.dataset.f === "group" && x.value === v; })[0];
      if (c) c.checked = true;
    });
    p.get("type") && p.get("type").split(",").forEach(function (v) {
      var c = controls.filter(function (x) { return x.dataset.f === "type" && x.value === v; })[0];
      if (c) c.checked = true;
    });
    if (p.get("code") === "1") { var c1 = controls.filter(function (x) { return x.dataset.f === "code"; })[0]; c1 && (c1.checked = true); }
    if (p.get("doi") === "1") { var c2 = controls.filter(function (x) { return x.dataset.f === "doi"; })[0]; c2 && (c2.checked = true); }
    if (p.get("ymin") && ymin) ymin.value = p.get("ymin");
    if (p.get("ymax") && ymax) ymax.value = p.get("ymax");
    if (p.get("q") && q) q.value = p.get("q");
  }

  controls.forEach(function (c) { c.addEventListener("change", apply); });
  ymin && ymin.addEventListener("input", apply);
  ymax && ymax.addEventListener("input", apply);
  q && q.addEventListener("input", apply);
  var clear = document.getElementById("lib-clear");
  clear && clear.addEventListener("click", function () {
    controls.forEach(function (c) { c.checked = true; });
    if (ymin) ymin.value = 2023;
    if (ymax) ymax.value = 2026;
    if (q) q.value = "";
    apply();
  });
  restore();
  apply();
})();
