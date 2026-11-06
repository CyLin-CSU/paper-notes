---
title: 首页
---

# ![CyLin-CSU](https://github.com/CyLin-CSU.png){ .h1-avatar } CyLin-CSU

> **最近更新**：<!-- LAST_UPDATE --> · <!-- ACTIVITY_BADGE --> · 精读 **27** 篇（含 1 篇 RF 跨领域、1 篇连接组学）· NeurIPS / ICLR / NMI 2023–2026 · 主题：EEG 基础模型与 Tokenization

个人论文精读库：记录研究问题、方法拆解与创新设计。++ctrl+k++ 全文搜索。

## :material-calendar-check: 活跃日程（最近一周）

<div class="ac-slot"><!-- ACTIVITY_CALENDAR --></div>

## :material-history: 更新时间线

<ul class="timeline" id="home-timeline" markdown>

- **2026-11-06** · 新增 [Uni-NTFM](papers/uni-ntfm.md) 精读，拆解时域与频域双向交叉注意力、分层拓扑嵌入和双域掩码重建。

- **2026-11-05** · 新增精读 REVE（NeurIPS 2025）：4D 傅里叶位置编码吃任意电极布局 + 92 数据集 61,415h 最大非侵入预训练语料——10 任务平均 +2.5%，linear probing 对 CBraMod +17%，对比集扩至十四篇

- **2026-11-04** · tokenization 线五篇齐发：NeuroRVQ（多尺度 RVQ，EEG 重构 MSE 较 LaBraM 降 67 倍）· BrainRVQ（时/频双域 RVQ）· CodeBrain（时/频双码本解耦）· NeuroDETR（VQ 事件记忆 + DETR 式事件检测，8 数据集 F1 全第一）· DELTA（RVQ + 掩码语言扩散 EEG-to-Text）——tokenization 演进页遗留缺口全面占坑

- **2026-11-04** · 新增精读 GUIDED（ATM · arXiv 2024）：EEG 映进 CLIP 空间 + 冻结 SDXL 两阶段引导扩散重建所见图像——站内「视觉重建」轴线第一篇，EEG 与 MEG/fMRI 首次同桌比较

- **2026-11-04** · 新增精读 CrossPT-EEG（arXiv 2024 · 清华）：16 人 × 22 session 视觉解码泛化基准——two-way ID 从被试内 0.95 崩到跨时间 0.51、跨被试 0.49，泛化代价的第一份系统账目

- **2026-11-04** · 新增精读 EEGArena（arXiv 2026）：30 FM × 25 监督基线 × 57 任务 / 23 数据集、五协议 2 万次评测——FM 大多领先但 TUEV 全体塌方，参数量不预测性能，预训练数据 0.6k→30k 小时无平台

- **2026-11-03** · 新增语音模型专题（与主题专题并列）：语音解码轴线按 Tokenization / Pretraining / 下游任务三段横读——脑端不切段、语音端选空间、监督对齐范式与检索/回归/生成三协议

- **2026-11-03** · 重整五个主题专题，合并通道适配与多任务；补入 NeuroRVQ、BrainRVQ、CodeBrain、NeuroDETR，更新写作说明。单篇笔记仍为 17 篇。

- **2026-11-02** · 新增精读 Défossez 语音解码（NMI 2023）：卷积脑模块对比对齐 wav2vec 2.0——3 秒 MEG 千余候选 zero-shot 检索所听语句，站内「语音解码」轴线的源头文献

- **2026-11-02** · 新增精读 SSM2Mel（arXiv 2025）：Mamba+MHSA 交替骨干重建连续语音 mel 谱——语音解码轴线从检索走向回归

- **2026-11-02** · 新增精读 LTFT（IEEE TETCI 2026）：逐频率复值窗口随梯度更新——频域学习从损失端（Not-All-EEG 加权）搬进变换核本身

- **2026-11-02** · 新增轴外精读 NPI（Nature Methods 2025）：把训好的网络当可干预的脑，虚拟扰动读出方向性全脑有效连接——「模型作科学工具」与站内「模型作解码器」对望

- **2026-10-28** · 新增精读 Not-All-EEG（arXiv 2026）：位置自适应时间调度——EMA 误差图把流匹配的全局 t 展开成通道×位置时间图，TS-FID 对 JET 再降 40–62%，生成轴线第三篇

- **2026-10-27** · 对比体系重构：comparison 收敛为枢纽页（速览 + 九维导读 + 战绩/互怼链），维度详解下放六大专题页，各专题覆盖扩至十二篇

- **2026-10-17** · 模型架构基础新增：图神经网络——消息传递 / 谱卷积 / GAT / 表达力边界，BrainGPT TEG 的机制基础

- **2026-10-17** · 新增精读 EEGDM（arXiv 2026）：潜扩散生成目标替代掩码重构——encoder 表示作扩散条件联合优化，TUEV 类不均衡指标全场最佳

- **2026-09-28** · 新增精读 CBraMod（ICLR 2025）：十字交叉注意力 + 非对称条件位置编码——EEG-FM-Compass 统一 benchmark 综合第一

- **2026-09-26** · 模型架构基础新增：生成模型三代脉络（VAE → DDPM → Flow Matching），一条主线串起 ELBO、得分匹配与速度场回归

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

- :material-heart-pulse:{ .lg .middle } **[BIOT](papers/biot.md)**
    ---
    NeurIPS 2023 · 3.2M 参数

    逐通道切段 + 线性注意力，跨格式生物信号统一编码的**起点**。tags: `tokenization` `线性注意力`

- :material-ear-hearing:{ .lg .middle } **[Défossez 语音解码](papers/defossez-speech.md)**
    ---
    NMI 2023

    脑信号与语音表示做**对比对齐**，从候选中检索听到的语音。tags: `对比学习` `语音解码`

- :material-brain:{ .lg .middle } **[LaBraM](papers/labram.md)**
    ---
    ICLR 2024 · 5.8M–369M 参数

    VQ 神经 codebook + 频谱重构 + 掩码码字预测的 EEG **大模型**。tags: `VQ-VAE` `掩码预训练`

- :material-magnify:{ .lg .middle } **[EEGPT](papers/eegpt.md)**
    ---
    NeurIPS 2024 · ~10M 参数

    表示对齐 + 掩码重构**双自监督**，linear probing 达 SOTA。tags: `双自监督` `线性探针`

- :material-chart-line:{ .lg .middle } **[BrainGPT](papers/braingpt.md)**
    ---
    arXiv 2024 · 至 1.09B 参数

    电极级建模 + GPT 式**自回归** + 任务共享电极图的首个 generalist。tags: `自回归` `多任务` `scaling law`

- :material-image:{ .lg .middle } **[GUIDED](papers/guided.md)**
    ---
    arXiv 2024 · 3.18M 编码器

    把 EEG 对齐到 **CLIP 空间**，引导预训练扩散模型重建所见图像。tags: `视觉重建` `扩散`

- :material-image-search:{ .lg .middle } **[CrossPT-EEG](papers/crosspt-eeg.md)**
    ---
    arXiv 2024

    比较被试内、跨被试与跨时间设定，评估**视觉解码的泛化能力**。tags: `视觉解码` `泛化评测`

- :material-robot:{ .lg .middle } **[NeuroLM](papers/neurolm.md)**
    ---
    ICLR 2025 · 至 1696M 参数

    把 EEG 当**外语接进 GPT-2**：文本对齐 tokenizer + 指令微调多任务。tags: `LLM` `指令微调`

- :material-compress:{ .lg .middle } **[LUNA](papers/luna.md)**
    ---
    NeurIPS 2025 · 7M–311M 参数

    用**可学习 query 汇聚通道**，把不同电极布局映射到固定隐空间。tags: `通道适配` `隐空间`

- :material-crosshairs-gps:{ .lg .middle } **[CBraMod](papers/cbramod.md)**
    ---
    ICLR 2025 · 4.0M 参数

    **十字交叉注意力**分别建模时间与通道关系，结合动态位置编码。tags: `掩码预训练` `时空建模`

- :material-music-note:{ .lg .middle } **[SSM2Mel](papers/ssm2mel.md)**
    ---
    arXiv 2025

    **Mamba 与注意力交替建模**，从 EEG 重建连续语音 mel 谱。tags: `状态空间模型` `语音解码`

- :material-hub-outline:{ .lg .middle } **[NPI](papers/surrogate-brain.md)**
    ---
    Nature Methods 2025

    对神经网络代理脑做**虚拟扰动**，估计脑区间的有效连接。tags: `虚拟扰动` `有效连接`

- :material-layers:{ .lg .middle } **[NeuroRVQ](papers/neurorvq.md)**
    ---
    arXiv 2025 · 5.9M 骨干

    **多尺度残差量化**结合幅值与相位约束，学习 EEG 离散词表。tags: `RVQ` `多尺度`

- :material-text-fields:{ .lg .middle } **[DELTA](papers/delta.md)**
    ---
    NeurIPS 2025 Workshop

    把 EEG 量化为离散 token，接入**掩码扩散语言模型**生成文本。tags: `EEG-to-Text` `掩码扩散`

- :material-sine-wave:{ .lg .middle } **[TFM-Tokenizer](papers/tfm-tokenizer.md)**
    ---
    ICLR 2026 · ~1.9M 参数

    单通道**时频 motif 词表**，离散 token 真正作为模型输入。tags: `tokenization` `时频motif`

- :material-swap-horizontal:{ .lg .middle } **[Uni-NTFM](papers/uni-ntfm.md)**
    ---
    ICLR 2026

    **双向交叉注意力**融合逐电极的波形和频带功率特征，再由 MoE Transformer 学习表示。tags: `时频融合` `MoE`

- :material-radio-tower:{ .lg .middle } **[RF-GPT](papers/rf-gpt.md)**
    ---
    arXiv 2026 · Qwen2.5-VL 3B/7B

    把射频**时频图接入视觉语言模型**，用合成数据训练信号理解能力。tags: `时频图` `多模态LLM`

- :material-creation:{ .lg .middle } **[JET](papers/jet.md)**
    ---
    ICML 2026 · 129.9M 参数

    **条件流匹配**结合生理结构约束，直接生成原始 EEG。tags: `流匹配` `EEG生成`

- :material-account-group:{ .lg .middle } **[EEGMoE](papers/eegmoe.md)**
    ---
    IEEE TNNLS 2026 · 1.68M 参数

    **域专属与共享专家**分别学习域差异和共性，用于 EEG 表示学习。tags: `MoE` `域解耦`

- :material-waveform:{ .lg .middle } **[EEGDM](papers/eegdm.md)**
    ---
    arXiv 2026 · 25M 参数

    用 EEG 表示引导**潜空间扩散**，通过去噪任务训练信号编码器。tags: `扩散` `表示学习`

- :material-timer-cog:{ .lg .middle } **[Not-All-EEG](papers/not-all-eeg.md)**
    ---
    arXiv 2026

    按位置难度调整**流匹配时间调度**，学习生成 EEG。tags: `流匹配` `时间调度`

- :material-chart-bell-curve-cumulative:{ .lg .middle } **[LTFT](papers/learnable-tf.md)**
    ---
    IEEE TETCI 2026

    把时频变换的**窗口函数设为可学习参数**，联合优化 EEG 分析前端。tags: `可学习前端` `时频变换`

- :material-compare:{ .lg .middle } **[BrainRVQ](papers/brainrvq.md)**
    ---
    arXiv 2026 · 5.82M 参数

    **时域与频域双路 RVQ**量化信号，按码字层级从粗到细预测。tags: `双域RVQ` `层级预测`

- :material-code:{ .lg .middle } **[CodeBrain](papers/codebrain.md)**
    ---
    ICLR 2026 · 15.17M 参数

    **时域与频域双码表**提供预测目标，多尺度骨干学习 EEG 表示。tags: `双码表` `状态空间模型`

- :material-radar:{ .lg .middle } **[NeuroDETR](papers/neurodetr.md)**
    ---
    arXiv 2026

    用**多尺度 VQ 事件记忆**，从连续 EEG 检测事件类别与起止时间。tags: `事件检测` `向量量化`

- :material-emoji-events:{ .lg .middle } **[EEGArena](papers/eegarena.md)**
    ---
    arXiv 2026

    在多任务与多种训练协议下，**统一评测 EEG 基础模型和监督模型**。tags: `基准评测` `EEG基础模型`

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

- :material-chart-timeline-variant:{ .lg .middle } **[生成模型脉络](basics/generative-lineage.md)**
    ---
    VAE → DDPM → Flow Matching

    一条主线：似然积分算不动——变分下界、逐步去噪、直连速度场的**三代绕法**。tags: `ELBO` `扩散` `流匹配`

- :material-graph:{ .lg .middle } **[图神经网络](basics/gnn.md)**
    ---
    消息传递 · GAT · 表达力

    网格与序列之外的第三种形态：置换不变聚合、谱卷积出身、过平滑边界——BrainGPT TEG 的机制基础。tags: `消息传递` `GAT` `图卷积`

</div>

## :material-sitemap: 主题专题

<div class="grid cards" markdown>

- :material-vector-link: **[EEG Tokenization 演进](topics/tokenization.md)**
    ---
    从规则切段到可学习词表：token 形态与词表用法的三步跃迁。

- :material-refresh: **[预训练范式对比](topics/pretraining.md)**
    ---
    对比学习 / 掩码建模 / 自回归三条路线与掩码目标的进化。

- :material-grid-large: **[通道适配与多任务学习](topics/multi-task.md)**
    ---
    脑电大模型的通道表示、空间整合与下游任务共享方式。

- :material-database: **[EEG 预训练数据全景](topics/data-landscape.md)**
    ---
    2500h vs 25000h：语料构成、域偏斜与规模瓶颈。

- :material-cube-outline: **[基座来源分析](topics/base-model.md)**
    ---
    主模型与 tokenizer 参数量，区分从零训练和加载现成基座。

- :material-ear-hearing: **[语音模型专题](topics/speech-models.md)**
    ---
    脑信号 → 语音：Défossez 检索范式与 SSM2Mel mel 回归的 tokenization / 预训练 / 下游任务横读。

- :material-earth: **[REVE](papers/reve.md)**
    ---
    NeurIPS 2025 · 12M / 69M / 408M

    **61,415h / 92 数据集**最大非侵入语料 + **4D 傅里叶位置编码**吃任意蒙太奇：10 任务平均 +2.5%，linear probing +17%。tags: `MAE` `4D位置编码` `线性探针`

</div>

## :material-chart-box-outline: 阅读统计

| 统计项 | 数值 |
|---|---|
| 精读论文 | 27 篇（EEG 基础模型 11 + tokenization 5 + EEG 生成 3 + 视觉解码 2 + 语音解码 2 + 基准评测 1 + 跨领域 RF 1 + 时频方法 1 + 连接组学 1） |
| 发表跨度 | 2023 – 2026 |
| 涉及会议/期刊 | NeurIPS ×3 + 1 WS · ICLR ×6 · ICML ×1 · TNNLS ×1 · NMI ×1 · Nature Methods ×1 · TETCI ×1 · arXiv ×11（另基础页 ICLR 2022 / CS336） |
| 主力预训练语料 | LaBraM 2500h · NeuroLM 25000h · BrainGPT 3750 万样本 · BIOT 1000 万样本 · CodeBrain/BrainRVQ TUEG 9200h+ |
| 模型规模跨度 | 0.89M（EEGMoE 激活）— 1.9B（Uni-NTFM 总参数） |

综合对比见 [十四篇方法对比](comparison.md)（枢纽页：一页速览 + 九维度导读——五个维度下放专题深读，模型设计 / 频域 / 规模效率保留在页内 + 论文互怼链）。

## :material-comment-processing: 留言板

欢迎留言交流——提问、纠错、推荐新论文都可以。

<div id="giscus-container" data-loading="lazy"></div>
