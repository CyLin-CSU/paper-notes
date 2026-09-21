// 按优先级依次尝试多个 CDN 加载 MathJax（国内网络友好，带超时与污染校验）
// CDN 顺序按实测速度：npmmirror 0.5s / jsdelivr 间歇 / unpkg 1.6s / bootcdn 9.2s
(function () {
  var cdns = [
    "https://registry.npmmirror.com/mathjax/3.2.2/files/es5/tex-mml-chtml.js",
    "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js",
    "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js",
    "https://cdn.bootcdn.net/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js"
  ];
  function tryLoad(i) {
    if (i >= cdns.length) {
      console.error("MathJax: 所有 CDN 均加载失败，公式保持原文显示");
      return;
    }
    var s = document.createElement("script");
    s.src = cdns[i];
    s.async = true;
    var settled = false;
    var timer = setTimeout(next, 8000); // 挂起兜底：8 秒超时强制切下一个 CDN
    function next() {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      s.onload = s.onerror = null;
      tryLoad(i + 1);
    }
    s.onload = function () {
      // 防"返回 200 但内容被污染/劫持"：校验 MathJax API 真的存在
      if (window.MathJax && window.MathJax.startup) {
        settled = true;
        clearTimeout(timer);
      } else {
        next();
      }
    };
    s.onerror = next;
    document.head.appendChild(s);
  }
  tryLoad(0);
})();
