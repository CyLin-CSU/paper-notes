---
title: 论文库
tags: [索引, 论文库]
---

# 论文库

> 34 篇精读的结构化目录，数据来自 `data/papers.json`。筛选为浏览器增强——禁用脚本时可完整浏览下方目录。想按方法维度横读请去[模型对比](models.md)与[十四篇方法对比](comparison.md)；查实验数值去[实验证据](evidence.md)。

<details class="lib-panel" markdown>
<summary>筛选与排序（点击展开）</summary>

<div class="lib-filters">

**类型**：<label><input type="checkbox" class="lib-f" data-f="type" value="research" checked> 研究</label> <label><input type="checkbox" class="lib-f" data-f="type" value="review" checked> 综述</label>

**分组**：<label><input type="checkbox" class="lib-f" data-f="group" value="fm" checked> 基础模型</label> <label><input type="checkbox" class="lib-f" data-f="group" value="generative" checked> 生成式</label> <label><input type="checkbox" class="lib-f" data-f="group" value="reviews" checked> 综述与观点</label> <label><input type="checkbox" class="lib-f" data-f="group" value="survey" checked> 相关研究</label>

**年份区间**：<input type="number" class="lib-y" id="lib-ymin" min="2023" max="2026" value="2023"> – <input type="number" class="lib-y" id="lib-ymax" min="2023" max="2026" value="2026">

**可用性**：<label><input type="checkbox" class="lib-f" data-f="code" value="1"> 有代码/项目页</label> <label><input type="checkbox" class="lib-f" data-f="doi" value="1"> 有 DOI</label>

**文本过滤**：<input type="search" id="lib-q" placeholder="标题 / 一句话摘要关键词">（筛选当前列表，全站全文搜索用页眉）

<button id="lib-clear" type="button">清除筛选</button>　当前显示 <b id="lib-count">34</b> / 34 篇

</div>

</details>

<div id="library-list" class="library-list">

<!-- LIBRARY_LIST -->

</div>

分享当前筛选：勾选条件后复制浏览器地址栏即可——筛选状态写入 URL 参数，接收方打开后自动恢复（[方案 §1](https://github.com/CyLin-CSU/paper-notes)）。

---

**相关阅读**：[模型对比](models.md) ｜ [实验证据](evidence.md) ｜ [数据集索引](datasets.md) ｜ [首页](index.md)
