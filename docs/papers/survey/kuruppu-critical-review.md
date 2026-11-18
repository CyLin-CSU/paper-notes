---
date: 2026-11-18
title: "EEG foundation models: a critical review of current progress and future directions"
authors: [Gayal Kuruppu, Neeraj Wagh, Vaclav Kremen, Yogatheesan Varatharajah]
venue: "J. Neural Eng. 2026"
year: 2026
tags: [综述, 批判性综述, 评测, scaling, 线性探针, OOD]
status: "精读"
rating: 4.5
arxiv: "https://doi.org/10.1088/1741-2552/ae4455"
code: "https://github.com/gayalkuruppu/eeg-foundation-models"
one-liner: "三支柱拆 10 个早期 EEG FM 后给出批判性结论：评测异质且多在分布内、scaling 证据弱、线性探针明显落后微调——SSL 表示质量存疑"
---

# EEG foundation models: a critical review of current progress and future directions

> **J. Neural Eng. 23, 021001（2026）· Topical Review · Open Access**

**作者**：Gayal Kuruppu、Neeraj Wagh（共同一作；UMN / UIUC）、Vaclav Kremen（Mayo Clinic）、Yogatheesan Varatharajah（通讯，UMN / Mayo Clinic）

## 1 问题定位

同期的综述（作者点名 Yao et al. 2025 等）偏技术组件（架构、SSL 策略），这篇自称补位的是**数据与领域视角**：早期 EEG FM 的真实成熟度、可长期追踪的评判标准。检索 2021-01–2024-09，收录 10 个 FM：BrainBERT、Neuro-GPT、Brant、BIOT、EEGFormer、LaBraM、Mentality（Mamba）、NeuroLM、FoME、BrainWave；多模态与 PSG 睡眠 FM 明确排除。数据规模用 **channel-hours** 口径（时长 × 通道数）：BrainBERT 4.5k → BrainWave 878k，TUEG 单库 541k。与其他综述的「小时数」口径不可直接互比。

## 2 三支柱对比

**输入表示**：多元时序 6/10（Brant、NeuroLM、FoME 等借此适配变通道）；功率谱 2/10（BIOT、EEGFormer）；时域+谱双输入 2/10（Brant、FoME）；时频表示 2/10（BrainBERT、BrainWave）。patch 粒度 1–6 s，上下文长度最长 90 s（FoME）——文中点出**没有任何 FM 能看 90 s 以上的长程模式**。

**建模与 SSL**：7/10 用掩码时序重构；只有 Neuro-GPT 在隐空间做因果掩码重构；BIOT 用 SimCLR 式对比；NeuroLM 通道条件阶梯式自回归。码本一族（LaBraM、NeuroLM、EEGFormer）用 VQ-VAE 式 tokenizer，用途各异——LaBraM 拿码字当重构目标、NeuroLM 接文本词表、EEGFormer 拿码本做可解释归因。

**评测**：任务数每篇 1（Mentality）到 12（BrainWave），多数 ≤5；4/10 的评测数据与预训练重叠（BrainBERT、Mentality、NeuroLM、FoME 均在分布内）；**只有 BrainWave 和 Brant 做过真正的 OOD 评测**。共享任务只有 TUAB 与 TUEV 两个（4 个模型可比）：TUAB AUC 0.86–0.92、TUEV F1 0.70–0.83；文中引证据说 TUAB 用传统方法已到 85–87% 精度，属饱和任务。

## 3 批判性结论（§5 的干货）

- **Scaling 证据弱**：预训练数据规模与 TUAB/TUEV 性能无正相关（LaBraM 数据最多却与 EEGFormer/NeuroLM 互有胜负）；LaBraM 自家曲线 ~1000 h 后趋平；模型缩放（3.3M–1.7B）只有边际改进。
- **线性探针显著落后微调**：五个报告 LP 的模型全线弱于 FT 与部分监督基线；FT 又略胜从头监督——作者据此**质疑 SSL 学到的表示质量**：增益可能主要来自架构与初始化而非预训练知识。
- **通用时序 FM 意外能打**：PatchTST / TimesNet 微调后在病理检测、睡眠分期可打平甚至超过 EEG FM；BrainWave 的实验里 MOMENT 在癫痫检测与病理检测超过 EEG FM。EEG 专属归纳偏置（空间建模、头皮+颅内联合）是 EEG FM 的反超点。
- **预处理普遍极简**：无显式去伪迹、归一化策略多数语焉不详，对 OOD 的影响未知。

## 4 未来方向三主题

基准与工具（对照既有特征范式并给统计检验、社区标准基准、进国际竞赛、低摩擦软件）；技术（整体评测框架、联邦学习、多模态预训练、蒸馏/剪枝做小模型）；应用（模型卡辅助选型、临床阅片辅助、按 SaMD 监管路径落地）。

## 5 站内视角

- 本篇的批判清单与 [EEGArena](eegarena.md) 高度互补：文中呼吁的「共享核心任务 + OOD + 强监督基线」正是 EEGArena 已经做成的事，两篇可当「诊断书与药方」连读。
- LP 落后 FT 的观察对本站 [REVE](../fm/reve.md) 微调策略（缓存 LP → 小学习率 FT）是个提醒：LP 短板在 EEG FM 里是普遍现象，不是单模型实现问题。
- 三支柱框架（输入表示 / 建模 / 评测）与本站 [预训练范式专题](../../topics/pretraining.md) 的「目标 / 掩码 / 范式」切分兼容，可交叉引用。

---

**相关阅读**

:material-sword-cross: [EEGArena（批判清单的落地实现）](eegarena.md) ｜ :material-format-list-bulleted: [Yao 综述（同刊前一年的技术面版本）](yao-eegfm-survey.md) ｜ :material-electric-bolt: [BrainGPT（文中 NeuroLM 的直接前身与对照）](../fm/braingpt.md) ｜ :material-tune: [REVE（LP/FT 差异与本站微调策略相关）](../fm/reve.md) ｜ :material-home: [首页](../../index.md)
