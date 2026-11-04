---
date: 2026-11-04
title: "Benchmarking EEG Foundation Models at Scale: Lessons from 20,000 Evaluations"
authors: [Zhige Chen, Shu Peng, Chengxuan Qin, Rui Liu, Rui Yang, Kay Chen Tan, Jibin Wu]
venue: "arXiv 2026"
year: 2026
tags: [基准评测, EEG基础模型, 监督基线, 预训练缩放, 通道鲁棒性]
status: "精读"
rating: 4.5
arxiv: "https://arxiv.org/abs/2609.32743"
code: "https://eeg.fm/benchmarks"
one-liner: "30 个 EEG FM × 25 个监督基线 × 57 任务/23 数据集、五协议 20,000+ 次评测:FM 大多领先、参数量不预测性能、固定架构下预训练数据 0.6k→30k 小时持续 +6.69pp——站内第一篇「基准评测」"
---
# Benchmarking EEG Foundation Models at Scale: Lessons from 20,000 Evaluations

> **arXiv 2026**

**作者**:Zhige Chen、Shu Peng、Chengxuan Qin(三人共同一作)、Rui Liu、Rui Yang、Kay Chen Tan、Jibin Wu(通讯,港理工)

## 1 问题定位:给 EEG FM 补一场有强对手的擂台赛

论文的出发点是既有基准的结构性缺陷(Table 1 清点了 11 个同类基准):监督基线普遍缺席或偏弱(EEG-FM-Bench、EEG-Bench 为 0,最多的 NeuralBench 也只有 8 个),且 FM 之间的排名把架构、参数量、预训练数据混在一起,赢了也说不清赢在哪。最终精度一个数字,还回答不了「预训练到底带来了什么」。EEG-Arena 的答案是把问题拆成五个 RQ:FM 对强基线(RQ1)、预训练收益及其随标签量的变化(RQ2)、参数量 scaling(RQ3)、预训练数据 scaling(RQ4)、通道配置鲁棒性(RQ5)——前一个靠大覆盖面横评,后四个靠受控对照实验,这是它区别于纯排行榜的地方。

## 2 基准设计

### 2.1 规模与模型口径

55 个模型 = 30 个 FM 变体 + 25 个基线(24 个 DL + YASA 谱方法);入选标准是开源可得、引用量、社区认可度。注意「30」是**变体口径**:20 个家族里 BIOT、LUNA、ST-EEGFormer、SleepFM 各 3 个变体、HEAR/REVE 各 2 个。57 个任务覆盖 7 范式(MI / Sleep / Clinical / Cognitive / AAD / ERP / Emotion;Table 4 逐任务给全定义,窗口 0.85–30 s、通道 2–144);有可靠被试元数据的任务同时报 WS(被试内)与 CS(跨被试)。

### 2.2 统一管线:统一什么、保留什么

软件包统一三件事:**数据**标准化为 HDF5(GDF/EDF 摄入,统一 split 与 10-20/10-10/10-5/动态通道选择);**模型**接口统一初始化与任务头配置,但**保留 FM 专属预处理与输入构造**(Table 7:21 套预处理并存——CBraMod 0.3–75 Hz + notch 60 + ÷100 µV,REVE session 级 z-score ±15σ 裁剪,而监督基线统一 0.1–75 Hz + notch 50 + 通道级 z-score);**训练/评估**统一(同一 split、按验证集选 checkpoint、统一优化设置)。两条排除规则很关键:预训练数据与下游数据直接重叠的结果被剔除出总排名(红 E 徽章),通道数/输入长度/格式不兼容的组合标记 unsupported 不进排名。

### 2.3 统计方法

三指标(二分类 balanced accuracy、多分类 macro-F1、Cohen's κ),对每个模型在每个任务上取三个指标名次的均值再对任务平均:

\[
\bar{r}_m = \frac{1}{|T_m|} \sum_{t \in T_m} \mathrm{rank}_t\!\left( \frac{r^{\mathrm{BA}}_{m,t} + r^{\mathrm{F1}}_{m,t} + r^{\kappa}_{m,t}}{3} \right)
\]

另有 Top-5 计数(进入任务前五的次数);双极 / 非双极设定分开排名。协议 II 的预训练增益定义为同架构 Full-FT 与随机初始化 Scratch-ST 的差:\( \bar{G}_m(d) = \bar{s}_m(d, \mathrm{Full\text{-}FT}) - \bar{s}_m(d, \mathrm{Scratch\text{-}ST}) \),在 6 档标签预算 {2%, 5%, 10%, 25%, 50%, 100%} 下配对比较。协议 IV 另用参数位移 \( P_{s,t} = \|\theta^{\mathrm{post}}_{s,t} - \theta^{\mathrm{pre}}_s\|_2 / \|\theta^{\mathrm{pre}}_s\|_2 \) 与逐层 1−CKA 度量微调改变了什么。

## 架构图

![Figure 1 · EEG-Arena 总览:(A) 开源软件包三接口;(B) 55 模型与 23 数据集 / 57 任务;(C) 五协议对应 RQ1–RQ5](../assets/eegarena-framework.png)

*Figure 1 · (A) 软件包:数据标准化(HDF5)→ 数据 / 模型 / 评估三接口,统一 trainer + evaluator,79,000+ 行代码;(B) 30 FM + 25 基线(2021–2026)与 7 范式 57 任务;(C) 协议 I 大横评、II 预训练收益 × 6 档标签预算、III 模型规模、IV 预训练数据 0.6k–30k h、V 通道子集鲁棒性*

---

**相关阅读**

:material-sword-cross: [CBraMod(「架构>规模」证据链在本榜被外部复现)](cbramod.md) ｜ :material-shield-search: [BIOT(双极设定内被追认为最强 FM)](biot.md) ｜ :material-tag-multiple: [TFM-Tokenizer(泛化项被本榜扣分的警示)](tfm-tokenizer.md) ｜ :material-puzzle: [NeuroRVQ(同批笔记:高方差画像与本榜一致)](neurorvq.md) ｜ :material-home: [首页](../index.md)
