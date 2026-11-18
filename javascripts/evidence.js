/* 实验证据筛选：按论文 / 数据集下拉过滤（渐进增强，无脚本时全部条目可见）。 */
(function () {
  "use strict";
  var list = document.getElementById("evidence-list");
  if (!list) return;
  var items = Array.prototype.slice.call(list.querySelectorAll(".ev-item"));
  var selPaper = document.getElementById("ev-paper");
  var selDataset = document.getElementById("ev-dataset");
  var count = document.getElementById("ev-count");
  if (!selPaper || !selDataset) return;

  var papers = {}, datasets = {};
  items.forEach(function (it) {
    if (it.dataset.paper) papers[it.dataset.paper] = true;
    if (it.dataset.dataset) datasets[it.dataset.dataset] = true;
  });
  Object.keys(papers).sort().forEach(function (k) {
    var o = document.createElement("option"); o.value = k; o.textContent = k; selPaper.appendChild(o);
  });
  Object.keys(datasets).sort().forEach(function (k) {
    var o = document.createElement("option"); o.value = k; o.textContent = k; selDataset.appendChild(o);
  });

  function apply() {
    var p = selPaper.value, d = selDataset.value, shown = 0;
    items.forEach(function (it) {
      var ok = (!p || it.dataset.paper === p) && (!d || it.dataset.dataset === d);
      it.style.display = ok ? "" : "none";
      if (ok) shown++;
    });
    if (count) count.textContent = shown;
    var url = new URL(location.href);
    p ? url.searchParams.set("paper", p) : url.searchParams.delete("paper");
    d ? url.searchParams.set("dataset", d) : url.searchParams.delete("dataset");
    try { history.replaceState(null, "", url); } catch (e) {}
  }

  var sp = new URLSearchParams(location.search);
  if (sp.get("paper")) selPaper.value = sp.get("paper");
  if (sp.get("dataset")) selDataset.value = sp.get("dataset");
  selPaper.addEventListener("change", apply);
  selDataset.addEventListener("change", apply);
  apply();
})();
