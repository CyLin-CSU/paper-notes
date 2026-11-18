/* 阅读清单：localStorage 收藏列表（保存/在读/已读），导出/导入带版本号 JSON。
   无脚本时页面显示使用说明。存储键 paper-notes.reading.v1 与单篇页「保存阅读」按钮共用。 */
(function () {
  "use strict";
  var list = document.getElementById("rl-list");
  if (!list) return;
  var KEY = "paper-notes.reading.v1";
  var STATUS = { saved: "待读", reading: "在读", done: "已读" };

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; }
  }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }

  function render() {
    var d = load();
    var ids = Object.keys(d);
    list.innerHTML = "";
    if (!ids.length) {
      list.innerHTML = '<p class="rl-empty">清单为空——在各论文笔记页点「保存阅读」加入。</p>';
      return;
    }
    ids.sort(function (a, b) { return (d[b].date || "").localeCompare(d[a].date || ""); });
    ids.forEach(function (pid) {
      var it = d[pid];
      var row = document.createElement("div");
      row.className = "rl-item";
      var sel = '<select data-id="' + pid + '">' + Object.keys(STATUS).map(function (s) {
        return '<option value="' + s + '"' + (it.status === s ? " selected" : "") + ">" + STATUS[s] + "</option>";
      }).join("") + "</select>";
      row.innerHTML = '<div><a href="../papers/reviews/' + pid + '/">' + (it.title || pid) +
        "</a><span class='rl-date'>加入于 " + (it.date || "?") + "</span></div>" + sel +
        "<button type='button' class='rl-del' data-id='" + pid + "'>移除</button>";
      list.appendChild(row);
    });
    list.querySelectorAll(".rl-item select").forEach(function (s) {
      s.addEventListener("change", function () { var d2 = load(); d2[s.dataset.id].status = s.value; save(d2); });
    });
    list.querySelectorAll(".rl-del").forEach(function (b) {
      b.addEventListener("click", function () { var d2 = load(); delete d2[b.dataset.id]; save(d2); render(); });
    });
  }

  var exp = document.getElementById("rl-export");
  exp && exp.addEventListener("click", function () {
    var blob = new Blob([JSON.stringify({ version: 1, items: load() }, null, 2)], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "paper-notes-reading-list.json";
    a.click();
  });

  var imp = document.getElementById("rl-import");
  var file = document.getElementById("rl-file");
  imp && file && imp.addEventListener("click", function () {
    var f = file.files && file.files[0];
    if (!f) { alert("先选择导出的 JSON 文件"); return; }
    var fr = new FileReader();
    fr.onload = function () {
      var d = load(), added = 0, updated = 0;
      try {
        var data = JSON.parse(fr.result);
        (data.items ? Object.keys(data.items) : []).forEach(function (k) {
          if (!d[k]) { d[k] = data.items[k]; added++; }
          else { d[k] = data.items[k]; updated++; }
        });
        save(d);
        alert("导入完成：新增 " + added + "，更新 " + updated);
        render();
      } catch (e) { alert("解析失败：" + e); }
    };
    fr.readAsText(f);
  });

  var clr = document.getElementById("rl-clear");
  clr && clr.addEventListener("click", function () {
    if (confirm("清空当前浏览器中的阅读清单？")) { save({}); render(); }
  });

  render();
})();
