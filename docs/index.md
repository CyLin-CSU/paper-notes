---
title: 首页
---

# ![CyLin-CSU](https://github.com/CyLin-CSU.png){ .h1-avatar } CyLin-CSU

> **最近更新**：<!-- LAST_UPDATE --> · <!-- ACTIVITY_BADGE --> · 精读 **6** 篇 · NeurIPS / ICLR 2023–2026 · 主题：EEG 基础模型与 Tokenization

个人论文精读库：记录方法拆解、创新点、流程与个人思考。`Ctrl + K` 全文搜索，[标签索引](tags.md) 按主题筛选。

## :material-calendar-check: 活跃日程（最近一周）

<!-- ACTIVITY_CALENDAR -->

## :material-history: 更新时间线

<!-- TIMELINE -->
<ul class="timeline" markdown>

- **2026-09-18** · 站点 v1.2：主页改版，新增更新时间线与活跃状态
- **2026-09-18** · 新增 3 个主题专题：Tokenization 演进 / 预训练范式 / 通道异构解法
- **2026-09-18** · 完成 6 篇精读：BIOT · LaBraM · EEGPT · BrainGPT · NeuroLM · TFM-Tokenizer

</ul>

## :material-bookshelf: 论文库

<div class="grid cards" markdown>

- :material-heart-pulse:{ .lg .middle } **[BIOT](papers/2026-09/0918-biot.md)**
    ---
    NeurIPS 2023 · 3.2M 参数

    逐通道切段 + 线性注意力，跨格式生物信号统一编码的**起点**。tags: `tokenization` `线性注意力`

- :material-brain:{ .lg .middle } **[LaBraM](papers/2026-09/0918-labram.md)**
    ---
    ICLR 2024 · 5.8M–369M 参数

    VQ 神经 codebook + 频谱重构 + 掩码码字预测的 EEG **大模型**。tags: `VQ-VAE` `掩码预训练`

- :material-magnify:{ .lg .middle } **[EEGPT](papers/2026-09/0918-eegpt.md)**
    ---
    NeurIPS 2024 · ~10M 参数

    表示对齐 + 掩码重构**双自监督**，linear probing 达 SOTA。tags: `双自监督` `线性探针`

- :material-chart-line:{ .lg .middle } **[BrainGPT](papers/2026-09/0918-braingpt.md)**
    ---
    arXiv 2024 · 至 1.09B 参数

    电极级建模 + GPT 式**自回归** + 任务共享电极图的首个 generalist。tags: `自回归` `多任务` `scaling law`

- :material-robot:{ .lg .middle } **[NeuroLM](papers/2026-09/0918-neurolm.md)**
    ---
    ICLR 2025 · 至 1696M 参数

    把 EEG 当**外语接进 GPT-2**：文本对齐 tokenizer + 指令微调多任务。tags: `LLM` `指令微调`

- :material-sine-wave:{ .lg .middle } **[TFM-Tokenizer](papers/2026-09/0918-tfm-tokenizer.md)**
    ---
    ICLR 2026 · ~1.9M 参数

    单通道**时频 motif 词表**，离散 token 真正作为模型输入。tags: `tokenization` `时频motif`

</div>

## :material-sitemap: 主题专题

<div class="grid cards" markdown>

- :material-vector-link: **[EEG Tokenization 演进](topics/tokenization.md)**
    ---
    从规则切段到可学习词表：token 形态与词表用法的三步跃迁。

- :material-refresh: **[预训练范式对比](topics/pretraining.md)**
    ---
    对比学习 / 掩码建模 / 自回归三条路线与掩码目标的进化。

- :material-grid-large: **[通道异构的四种解法](topics/spatial.md)**
    ---
    通道 embedding / 空间编码 / 单通道独立 / 图结构整合，跨设备能力的分水岭。

</div>

## :material-chart-box-outline: 阅读统计

| 统计项 | 数值 |
|---|---|
| 精读论文 | 6 篇 |
| 发表跨度 | 2023 – 2026 |
| 涉及会议 | NeurIPS ×2 · ICLR ×3 · arXiv ×1 |
| 预训练语料规模（论文合计） | 2500h + 25000h + 3750 万样本 |
| 模型规模跨度 | 1.9M — 1.09B |

综合对比见 [六篇方法对比](comparison.md)（13 个维度总览表 + 演进脉络）。
