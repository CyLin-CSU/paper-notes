---
title: 首页
---

# ![CyLin-CSU](https://github.com/CyLin-CSU.png){ .h1-avatar } CyLin-CSU

> **最近更新**：<!-- LAST_UPDATE --> · <!-- ACTIVITY_BADGE --> · 精读 **7** 篇（含 1 篇 RF 跨领域）· NeurIPS / ICLR 2023–2026 · 主题：EEG 基础模型与 Tokenization

个人论文精读库：记录方法拆解、创新点、流程与个人思考。++ctrl+k++ 全文搜索。

## :material-calendar-check: 活跃日程（最近一周）

<div class="ac-slot"><!-- ACTIVITY_CALENDAR --></div>

## :material-history: 更新时间线

<ul class="timeline" id="home-timeline" markdown>

- **2026-09-24** · 新增双篇精读：EEGMoE（域解耦 MoE）× LUNA（拓扑统一）——通道异构问题的两条相反路线；专题页新增第五/六种解法

- **2026-09-23** · 新增精读 JET（ICML 2026）：条件流匹配生成原始 EEG + 三条生理结构约束——站内首篇「生成」轴线论文

- **2026-09-22** · 模型架构基础新增：Attention 替代方案（线性注意力 → Mamba-2 → Gated DeltaNet → 混合 → DSA），整理自 Stanford CS336 Lec 4

- **2026-09-21** · 新增跨领域精读：RF-GPT——射频时频图 + 多模态 LLM（RFLM 概念首作）

- **2026-09-21** · 新增分类「模型架构基础」：首篇 LoRA 低秩适配精读（原论文 + 变体族谱 + EEG 语境用法）

- **2026-09-20** · 全站内容审查：2 个审查代理核查 21 处问题并全部修复（含数据集矩阵严重错误）

- **2026-09-19** · 新增专题：基座来源分析（从零训练 vs 现成 Base Model）

- **2026-09-19** · 数据集索引新增 数据集×论文 使用矩阵热力图

- **2026-09-18** · 组件大升级：Mermaid 流程图/内容标签页/脚注/术语提示/图片放大/阅读进度条/对比图表

- **2026-09-18** · 新增自问自答区、参考文献索引、数据集索引；移除活跃热力图；修复数学公式渲染
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

- :material-radio-tower:{ .lg .middle } **[RF-GPT](papers/2026-09/0921-rf-gpt.md)** `跨领域`
    ---
    arXiv 2026 · Qwen2.5-VL 3B/7B

    射频**时频图当图片**喂进多模态 LLM，纯合成数据零人工标注。tags: `时频图` `多模态LLM` `合成数据`

- :material-creation:{ .lg .middle } **[JET](papers/2026-09/0923-jet.md)** `EEG 生成`
    ---
    ICML 2026 · 129.9M 参数

    条件流匹配直接生成**原始 EEG**，三条生理结构约束，TS-FID 降 40%+。tags: `Flow Matching` `EEG生成`

- :material-account-group:{ .lg .middle } **[EEGMoE](papers/2026-09/0924-eegmoe.md)** `MoE`
    ---
    IEEE TNNLS 2026 · 1.68M 参数

    Specific+Shared 双专家**解耦域差异**：Top-K 管特性、软路由管共性。tags: `MoE` `域解耦` `多任务`

- :material-compress:{ .lg .middle } **[LUNA](papers/2026-09/0924-luna.md)** `拓扑无关`
    ---
    NeurIPS 2025 · 7M–311M 参数

    学习 query 把任意电极拓扑**压进固定隐空间**：通道线性复杂度，FLOPs 降 300×。tags: `跨导联` `Perceiver` `效率`

</div>

## :material-cube-unfolded: 模型架构基础

大模型通用组件的精读与速查——与 EEG 无关也值得掌握的基本功。

<div class="grid cards" markdown>

- :material-angle-acute:{ .lg .middle } **[LoRA · 低秩适配](basics/lora.md)**
    ---
    ICLR 2022 · 微调 0.02% 参数

    冻结底座 + 低秩旁路 BA：参数高效微调的**事实标准**，含变体族谱与 EEG 用法。tags: `LoRA` `参数高效微调`

- :material-vector-polyline:{ .lg .middle } **[Attention 替代方案](basics/attention-alternatives.md)**
    ---
    Stanford CS336 Lec 4 · MoE 之前部分

    长上下文路线图：线性注意力 → Mamba-2 → Gated DeltaNet → 混合堆叠 → DSA 稀疏注意力。tags: `线性注意力` `SSM` `稀疏注意力`

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

- :material-database: **[EEG 预训练数据全景](topics/data-landscape.md)**
    ---
    2500h vs 25000h：语料构成、域偏斜与规模瓶颈。

- :material-cube-outline: **[基座来源分析](topics/base-model.md)**
    ---
    五篇从零训练，唯一例外 NeuroLM 站在 GPT-2 上——为什么。

- :material-vector-circle: **[多任务三条路线](topics/multi-task.md)**
    ---
    逐任务微调 / 共享骨干联合训练 / 指令微调。

</div>

## :material-chart-box-outline: 阅读统计

| 统计项 | 数值 |
|---|---|
| 精读论文 | 10 篇（EEG 8 + 跨领域 RF 1 + EEG 生成 1） |
| 发表跨度 | 2023 – 2026 |
| 涉及会议/期刊 | NeurIPS ×3 · ICLR ×3 · ICML ×1 · TNNLS ×1 · arXiv ×2（另基础页 ICLR 2022 / CS336） |
| 主力预训练语料 | LaBraM 2500h · NeuroLM 25000h · BrainGPT 3750 万样本 · BIOT 1000 万样本 |
| 模型规模跨度 | 0.89M（EEGMoE 激活）— 1.09B（按各篇主模型口径） |

综合对比见 [十篇方法对比](comparison.md)（核心六篇 14 维表 + 扩展四篇速览 + benchmark 战绩 + 互怼链）。

## :material-comment-processing: 留言板

欢迎留言交流——提问、纠错、推荐新论文都可以。

<div id="giscus-container" data-loading="lazy"></div>
