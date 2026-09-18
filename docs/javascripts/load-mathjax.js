// 按优先级依次尝试多个 CDN 加载 MathJax（国内网络友好）
(function () {
  var cdns = [
    "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js",
    "https://cdn.bootcdn.net/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js",
    "https://registry.npmmirror.com/mathjax/3.2.2/files/es5/tex-mml-chtml.js",
    "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js"
  ];
  function tryLoad(i) {
    if (i >= cdns.length) {
      console.warn("MathJax: 所有 CDN 均加载失败");
      return;
    }
    var s = document.createElement("script");
    s.src = cdns[i];
    s.async = true;
    s.onerror = function () { tryLoad(i + 1); };
    document.head.appendChild(s);
  }
  tryLoad(0);
})();
