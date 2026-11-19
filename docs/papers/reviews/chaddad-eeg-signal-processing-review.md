---
date: 2026-11-19
title: "Electroencephalography Signal Processing: A Comprehensive Review and Analysis of Methods and Techniques"
authors: [Ahmad Chaddad, Yihang Wu, Reem Kateb, Ahmed Bouridane]
venue: "Sensors 2023"
year: 2023
tags: [综述, EEG, 信号处理, 去噪, 特征工程, 传统机器学习]
status: "精读"
rating: 3
doi: "10.3390/s23146434"
arxiv: ""
code: ""
one-liner: "传统流水线视角的 EEG 信号处理综述：采集→去噪（回归/BSS/CCA/小波/EMD，公式+伪代码）→特征工程（时频/高阶谱/非线性）→分类（ML+DL）四阶段方法对照；全文零处基础模型"
---

# Electroencephalography Signal Processing: A Comprehensive Review and Analysis of Methods and Techniques

> **Sensors 23(14):6434（2023）· Review**

**作者**：Ahmad Chaddad, Yihang Wu, Reem Kateb（Taibah University，沙特）+ 桂林电子科技大学 + Ahmed Bouridane（University of Sharjah，阿联酋）

## 1 问题定位与收录范围

EEG 信号信噪比低、非平稳、非线性、个体差异大，直接从原始信号提取任务信息困难——综述把解法组织成**采集 → 去噪 → 特征工程 → 分类**四阶段流水线（原文 Figure 2 与伪代码 Algorithm 1），逐阶段比较方法优劣。检索范围是"主要科学与工程数据库"，未给检索式与筛选流程（无 PRISMA；对照站内 [Yao 综述](yao-eegfm-survey.md) 的 PRISMA 协议），收录文献到 2023 年中。

**全文零处 foundation model / pretraining**（站内检索原文确认）——它是一篇传统信号处理方法学综述，与站内四篇 FM 综述不在同一轴上。站内价值：FM 综述里反复出现的痛点（预处理极简、参考电极选择、容积传导）在这篇里有系统的方法学展开，是那一层的教科书底座。

## 2 四阶段方法对照

### 2.1 采集

侵入式 vs 非侵入式两条路线；便携设备单列一节——Emotiv EPOC（14 通道）、Muse 头带（10–20 系统 4 记录电极 AF7/AF8/TP9/TP10 + 参考 Fpz，用于卒中识别）等，代价是通道少、精度低。参考电极的选择问题在采集阶段就提出：EEG 记录的是活动电极与参考电极的电位差，参考点选在哪，数据就长什么样。

### 2.2 去噪（全文最重的一章）

| 方法族 | 代表 | 论文给出的局限 |
|---|---|---|
| 回归法 | 以参考通道回归去除伪迹 | 双向污染（参考通道本身含脑电成分） |
| 盲源分离 | ICA、PCA | ICA 难以完全分离 EMG 伪迹；PCA 分离依据方差排序、不保证成分对应源 |
| 典型相关分析 | CCA | 依赖通道间相关性假设 |
| 小波变换 | DWT/小波阈值 | 缺平移不变性，阈值选取敏感 |
| 经验模态分解 | EMD | 模态混叠、端点效应 |

去噪效果评价指标一并给出公式（原文式 8）：MSE、RMSE、SNR、PRD。每个方法族配数学公式与伪代码——这是论文自认的独特贡献（原 Introduction："comprehensive description of denoising techniques, which includes mathematical formulations with pseudocodes"）。

### 2.3 特征工程

三类：时频分析（STFT/小波相干等，癫痫/情绪场景）、高阶谱分析（超出二阶统计，捕捉非线性耦合）、非线性动力学分析（Lyapunov 指数、熵等，对应 EEG 的非平稳非线性本质）。这层在 FM 论文里被 patch 化+深层网络整体替换，但特征选择逻辑（频带差异、非平稳性）仍在解释 FM 失败案例时有效。

### 2.4 分类

传统 ML（SVM/KNN/随机森林/决策树）与 DL（CNN/RNN/GAN）两大族并列，应用表覆盖癫痫（CHB-MIT）、情绪（DEAP、SEED 系列）、运动想象（BCI Competition IV）、SSVEP、ADHD 等。结论口径：ML 在 EEG 分类上可达高准确率；DL 简化了流程（端到端），在癫痫发作检测上与 ML 准确率相当，但需要更大数据量（原文 §3）。

## 3 挑战与展望（原文 §3）

挑战五条：噪声与非平稳；**容积传导**（多源信号叠加，源定位困难）；**参考电极选择**（选点不同则数据不同）；个体差异；深度学习可解释性。展望三条：XAI（Smooth-Grad 类方法已用于情绪识别与棘波检测）、域适应、联邦学习。

## 4 证据边界与站内视角

- 综述自身无实验，评价性结论均为转述（如"DL 与 ML 在癫痫检测准确率相当"注明为文献综合口径）；无 PRISMA 检索协议，收录范围不可复现。
- 与站内 FM 综述的分工：[Yao](yao-eegfm-survey.md) / [Chen](chen-representation-learning-review.md) 记录 FM 现状，[Kuruppu](kuruppu-critical-review.md) 批判评测，[Kwon](kwon-neural-fm-perspective.md) 给规范主张，本篇补**传统信号处理方法学底盘**——FM 论文集体跳过的去噪与特征工程环节在这里有完整方法清单；[Kuruppu §5.1](kuruppu-critical-review.md) 批评 FM「Minimal data preprocessing」，本文即该环节的背景文献。
- 时间边界：2023 年中截稿，无任何基础模型/大规模预训练内容；引用它定位「传统四阶段范式」即可，不要引它描述 FM 现状。

---

**相关阅读**

:material-vector-link: [预训练范式对比（本文的去噪/特征两阶段在 FM 里被掩码建模整体替换）](../../topics/pretraining.md) ｜ :material-clipboard-check: [Kuruppu 批判综述（「Minimal data preprocessing」的出处）](kuruppu-critical-review.md) ｜ :material-book-open-variant: [Yao FM 综述（有 PRISMA 协议的对照面）](yao-eegfm-survey.md) ｜ :material-lighthouse: [EEGArena（FM 时代的统一评测）](../survey/eegarena.md)
