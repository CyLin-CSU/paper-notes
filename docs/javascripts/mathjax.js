window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    // 跳过整页，仅处理 arithmatex 扩展生成的公式节点
    ignoreHtmlClass: ".*",
    processHtmlClass: "arithmatex"
  }
};
