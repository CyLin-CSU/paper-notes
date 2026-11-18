---
date: 2026-11-18
title: "Foundation models for EEG decoding: current progress and prospective research"
authors: [Yuxuan Yao, Hongbo Wang, Li Chen, Yiheng Peng, Jingjing Luo]
venue: "J. Neural Eng. 2025"
year: 2025
tags: [综述, EEG基础模型, 掩码重构, 自回归, 预训练策略, 范式失衡]
status: "精读"
rating: 4
doi: "10.1088/1741-2552/ae17e9"
arxiv: ""
code: ""
one-liner: "PRISMA 综述 + 自跑 10 模型 × 6 数据集：掩码重建是主流预训练路线，FM 赢临床域、输 MI 域，根子在预训练数据被癫痫范式主导"
---

# Foundation models for EEG decoding: current progress and prospective research

> **J. Neural Eng. 22, 061002（2025）· Topical Review**

**作者**：Yuxuan Yao、Hongbo Wang、Li Chen、Yiheng Peng（复旦工研院 AIR）、Jingjing Luo（通讯，中南大学）

## 1 问题定位

监督式 EEG 模型任务特定、数据依赖重。本文用 PRISMA 流程筛 EEG-only、含预训练、有泛化评测的近五年工作，按「任务与数据集 / 预训练策略 / 架构」三条线梳理，并补一场统一协议的性能对比。特色是**自己跑了对比实验**：10 个模型 × 6 个数据集，原论文报告值（彩色）与自跑补齐值（黑色）分开标注。

## 2 任务与数据集：范式失衡

五个下游任务域（癫痫 / MI / 情绪 / 睡眠 / 其他）的常用数据集汇总成表，按总时长一排就看出口径差距：

| 任务域 | 被试数 | 总时长 |
|---|---|---|
| 癫痫（TUEG 系） | 14 987 | 27 062 h |
| 睡眠分期 | 347 | 6 035 h |
| 情绪识别 | 275 | 193 h |
| 运动想象 | 272 | 152 h |

§3.5 是全文最有价值的论点：现有 FM 预训练基本被 TUEG 一类临床癫痫数据主导，与 MI / 情绪等下游范式差异大，形成域差；文中引的一项研究显示部分预训练模型从头训练还不如任务专用模型。多范式联合预训练是数据侧的待解问题。

## 3 预训练策略分类

**生成式**三分支：

- 自编码器重构：EEGFormer 加 VQ 码本、DFformer 用类 token 生成基矩阵重构。
- 掩码重构：主流路线。掩码粒度分通道级（TSP）与 patch 级（随机 / 块状）；重建空间分信号级（MAE 式，最常用）、embedding 级（BERT 式）、离散级（BEiT 式 VQ，LaBraM）；EEG2Rep 为 EEG 定制语义子序列保留（SSP）掩码。
- 自回归：BrainGPT（站内命名，原文标 EEGPT(2)）因果单向预测未来信号。

**多域重构**：空间走 MMM 拓扑建模与 GMAEEG 图掩码；频率走 Neuro-BERT 傅里叶反演预测、LaBraM 的 VQ 神经频谱预测。

**对比式**：增广不变型至今没出现在 EEG FM 里（归因：各任务增广需求不一致）；结构型只有 CPC 一支（BENDR、TSP）。

三条作者口径的观察：掩码率 ~50%，低于图像的 75–90%，解释是 EEG 语义冗余低；AR 与时序结构天然契合但受非平稳、低 SNR 拖累；同架构对照（BrainGPT，站内口径）睡眠分期 AR 77.9% > MAE 74.8%，由此推测 **AR 适合时间连续任务、掩码适合信号突变任务（如棘波癫痫）**——尚属初步结论。

## 4 架构组件

切段分 instance-wise（逐时间窗、含全部通道，单数据集）与 channel-wise（逐通道 patch，跨导联配置）。位置编码以可学习静态为主，正弦余弦因采样率绑定而少见；动态方向有 RoPE（EEGPT，站内口径 Wang et al.）与条件位置编码（CBraMod 非对称双轴）；空间信息两条路——可学习通道嵌入 vs 电极物理 2D/3D 坐标（TSP、MMM）。骨干 encoder-only 一边倒，Mamba 只有 FEMBA。注意力变体：时空分离注意力、CBraMod 十字交叉、EEG2Rep 交叉注意力。

## 5 自跑对比：临床域赢、MI 域输

协议：6 数据集（TUAB / TUEV / BCIC IV-2a·2b / SleepEDFx / SEED-V），统一预训练权重 + 全参微调，50 epoch AdamW，不支持变通道的模型前置一个空间滤波卷积；MI 用 LOSO。

- **临床域 FM 大胜**：自跑口径 Neuro-GPT 在 TUAB 0.7889 / TUEV 0.5501 领先，超过 EEGNet（0.7642 / 0.3876）——作者归因于预训练域与癫痫数据同源。
- **MI 全线失守**：EEGNet 两个数据集最高（2a 0.6879 / 2b 0.7321），BENDR 2a 仅 0.4899，EEGPT 0.5846。低 SNR + 范式域差双重归因。
- **中间地带**：LaBraM-Base / CBraMod 在 SleepEDFx 0.6771 / 0.6221、SEED-V 0.4095 / 0.4091 尚有竞争力。
- 成本注脚：EEGNet 0.003M 参数，Neuro-GPT 56.6M——增益换参数。

## 6 讨论与展望

可解释性盘了 Grad-CAM（CBraMod 的 MI 任务激活落在 C3/C4 运动皮层）与时序显著性图（EEGFormer 的癫痫段落在 Fz/Pz/T3/T6）；可信性盘了扰动鲁棒（EEG2Rep 高斯噪声等扰动下最多降 3.21%）；并把「幻觉」拆成两类——关注无关区域仍给出置信预测、不看任务特征碰对答案。未来方向四条：信号导向的 pretext 任务、EEG 定制对比学习框架、注意力机制优化、多模态 SSL（卡在对齐数据稀缺）。

## 7 站内视角

- 本文与 [EEGArena](eegarena.md) 互补：一个纵评预训练策略（固定协议自跑），一个横评 FM 对监督基线（各模型专属预处理）。MI 结论不一致（EEGArena 称 FM 大多领先，本文称 FM 输 EEGNet），协议与任务池不同，站内不做合并推断。
- 命名陷阱：文中 EEGPT(1) = 站内 [EEGPT](../fm/eegpt.md)（Wang et al., NeurIPS 2024），EEGPT(2) = 站内 [BrainGPT](../fm/braingpt.md)（Yue et al.）。引用两篇时注意消歧。
- §3.5 的域差论证是数据侧动机的直接引文，[数据全景专题](../../topics/data-landscape.md) 可对接。

---

**相关阅读**

:material-format-list-bulleted: [EEGArena（互为镜像的评测视角）](eegarena.md) ｜ :material-shield-search: [CBraMod（本榜临床域自跑第一梯队）](../fm/cbramod.md) ｜ :material-electric-bolt: [BrainGPT（文中 EEGPT(2)，AR vs MAE 同架构对照）](../fm/braingpt.md) ｜ :material-cog: [预训练范式专题（目标/掩码/范式同一口径）](../../topics/pretraining.md) ｜ :material-script-text: [站内 EEG 基础模型综述（可对照其取舍）](../../blog-2023-2026.md) ｜ :material-home: [首页](../../index.md)
