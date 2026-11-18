---
title: 模型对比
tags: [索引, 模型对比, 工具]
---

# 模型对比

> 从 `data/models.json`（21 个模型条目）中选择 2–4 个模型并排对照。数值只在与协议条件相符时同表显示；跨论文条件不同可并列查看原报告，本页**不做综合得分或默认排名**。十四篇的叙事性对照见[十四篇方法对比](comparison.md)。

## 选择模型 {: #pick }

<div class="mdl-picker">

<div class="mdl-chips" id="mdl-chips"></div>

<p>已选 <b id="mdl-count">0</b> / 4：<span id="mdl-selected">（未选择）</span>　<button id="mdl-clear" type="button">清空</button></p>

</div>

<div id="mdl-table-wrap" class="mdl-table-wrap">

<!-- MODELS_FALLBACK -->

</div>

<script type="application/json" id="models-data"></script>

## 使用规则 {: #使用规则 }

- **参数量**按口径分组（总参数 / 激活 / encoder / tokenizer），来自各论文自报，口径见 [comparison.md 规模节](comparison.md#mod-scale)；
- **权重状态**：open = 官方开源；partial = 以项目页为准；none = 未放出；
- **布局**一栏描述模型对电极配置的假设（固定 10-20 / ACPE 非绑定 / query 压缩 / 坐标生成），是影响跨数据集泛化的主要设计因素；
- 引用任何数值请附论文版本与表号——[实验证据页](evidence.md)的每条数值都带出处，可直接链接。

---

**相关阅读**：[实验证据](evidence.md) ｜ [论文库](library.md) ｜ [十四篇方法对比](comparison.md) ｜ [首页](index.md)
