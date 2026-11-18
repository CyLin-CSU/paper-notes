/* 模型对比：从内嵌 JSON 选 2–4 个模型逐字段并排。
   无脚本时页面展示全部模型的静态回退表（构建时生成）。 */
(function () {
  "use strict";
  var dataEl = document.getElementById("models-data");
  var chips = document.getElementById("mdl-chips");
  if (!dataEl || !chips) return;
  var models;
  try { models = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var byId = {};
  models.forEach(function (m) { byId[m.model_id] = m; });

  var selected = [];
  var MAX = 4;
  var wrap = document.getElementById("mdl-table-wrap");
  var countEl = document.getElementById("mdl-count");
  var selLabel = document.getElementById("mdl-selected");
  var FIELDS = ["params_m", "input", "layout", "training_stage", "weights_note"];
  var FIELD_LABELS = { params_m: "参数量 (M)", input: "输入", layout: "电极布局适配", training_stage: "训练阶段", weights_note: "权重与许可" };

  function renderChips() {
    chips.innerHTML = "";
    var groups = {};
    models.forEach(function (m) { (groups[m.paper_id] = groups[m.paper_id] || []).push(m); });
    Object.keys(groups).sort().forEach(function (pid) {
      var g = document.createElement("span");
      g.className = "mdl-group";
      g.innerHTML = "<b>" + pid + "</b>：";
      groups[pid].forEach(function (m) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "mdl-chip" + (selected.indexOf(m.model_id) !== -1 ? " on" : "");
        b.textContent = m.name;
        b.title = m.model_id;
        b.addEventListener("click", function () { toggle(m.model_id); });
        g.appendChild(b);
        g.appendChild(document.createTextNode(" "));
      });
      chips.appendChild(g);
    });
  }

  function toggle(id) {
    var i = selected.indexOf(id);
    if (i !== -1) selected.splice(i, 1);
    else {
      if (selected.length >= MAX) return;
      selected.push(id);
    }
    renderChips();
    renderTable();
  }

  function renderTable() {
    if (countEl) countEl.textContent = selected.length;
    if (selLabel) selLabel.textContent = selected.length ? selected.map(function (id) { return byId[id].name; }).join(" · ") : "（未选择）";
    if (!wrap) return;
    if (selected.length < 2) {
      wrap.querySelectorAll(".mdl-compare").forEach(function (n) { n.remove(); });
      wrap.querySelectorAll(".models-fallback").forEach(function (n) { n.style.display = ""; });
      return;
    }
    wrap.querySelectorAll(".models-fallback").forEach(function (n) { n.style.display = "none"; });
    var old = wrap.querySelector(".mdl-compare");
    if (old) old.remove();
    var t = document.createElement("table");
    t.className = "mdl-compare";
    var head = "<thead><tr><th>字段</th>" + selected.map(function (id) {
      var m = byId[id];
      return "<th>" + m.name + (m.weights === "open" ? " ✓开源" : m.weights === "none" ? " ✗无权重" : " △部分") + "</th>";
    }).join("") + "</tr></thead>";
    var body = FIELDS.map(function (f) {
      return "<tr><th>" + FIELD_LABELS[f] + "</th>" + selected.map(function (id) {
        var v = byId[id][f];
        return "<td>" + (v === null || v === undefined ? "—" : String(v)) + "</td>";
      }).join("") + "</tr>";
    }).join("");
    var foot = "<tr><th>条目 id</th>" + selected.map(function (id) { return "<td><code>" + id + "</code></td>"; }).join("") + "</tr>";
    t.innerHTML = head + "<tbody>" + body + foot + "</tbody>";
    var share = document.createElement("p");
    share.className = "mdl-share";
    var url = new URL(location.href);
    url.searchParams.set("m", selected.join(","));
    share.innerHTML = '比较链接：<input readonly value="' + url.toString() + '" onclick="this.select()">';
    t.appendChild(document.createElement("tbody"));
    var d = document.createElement("div");
    d.appendChild(t); d.appendChild(share);
    d.className = "mdl-compare";
    wrap.appendChild(d);
  }

  var mp = new URLSearchParams(location.search).get("m");
  if (mp) mp.split(",").slice(0, MAX).forEach(function (id) { if (byId[id] && selected.indexOf(id) === -1) selected.push(id); });
  renderChips();
  renderTable();
})();
