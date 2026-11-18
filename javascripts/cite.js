/* 单篇页工具条：复制 BibTeX 引用 + 保存阅读（localStorage，方案 G）。
   无脚本时来源链接照常可点，按钮不显示。 */
(function () {
  "use strict";
  var bars = document.querySelectorAll(".paper-toolbar");
  if (!bars.length) return;
  var KEY = "paper-notes.reading.v1";

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; }
  }
  function save(d) {
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {}
  }

  bars.forEach(function (bar) {
    var pid = bar.dataset.paper;
    var cite = bar.querySelector(".pt-cite");
    var saveBtn = bar.querySelector(".pt-save");
    if (cite) {
      cite.addEventListener("click", function () {
        var text = "";
        try { text = JSON.parse(cite.dataset.cite); } catch (e) { text = cite.dataset.cite; }
        function done() {
          cite.textContent = "已复制 ✓";
          setTimeout(function () { cite.textContent = "复制引用"; }, 1600);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, done);
        } else {
          var ta = document.createElement("textarea");
          ta.value = text; document.body.appendChild(ta); ta.select();
          document.execCommand("copy"); document.body.removeChild(ta); done();
        }
      });
    } else {
      cite && (cite.style.display = "none");
    }
    if (saveBtn) {
      function refresh() {
        var d = load();
        saveBtn.textContent = d[pid] ? "已保存 ✓" : "保存阅读";
        saveBtn.classList.toggle("on", !!d[pid]);
      }
      saveBtn.addEventListener("click", function () {
        var d = load();
        if (d[pid]) { delete d[pid]; } else {
          d[pid] = { paper_id: pid, title: saveBtn.dataset.title || pid,
                     status: "saved", date: new Date().toISOString().slice(0, 10) };
        }
        save(d); refresh();
      });
      refresh();
    }
  });
})();
