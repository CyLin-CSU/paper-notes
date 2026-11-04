---
date: 2026-09-24
title: "EEGMoE: A Domain-Decoupled Mixture-of-Experts Model for Self-Supervised EEG Representation Learning"
authors: [Xuange Gao, Danli Wang, Yanyan Zhao]
venue: "IEEE TNNLS 2026"
year: 2026
tags: [MoE, 域解耦, 自监督预训练, 多任务, 情绪识别, 运动想象]
status: "精读"
rating: 4
doi: "10.1109/TNNLS.2026.3652277"
one-liner: "用 Specific+Shared 双专家组把 EEG 的域共性与域特性分开学：Top-K 路由管特性、软路由管共性"
---
# EEGMoE: A Domain-Decoupled Mixture-of-Experts Model for Self-Supervised EEG Representation Learning

> **IEEE TNNLS 2026**

**作者**：Xuange Gao, Danli Wang, Yanyan Zhao（State Key Laboratory of Multimodal Artificial Intelligence Systems, CASIA）

## 1 问题定位：统一格式 ≠ 学好表征

任务专用 EEG 模型（DEAP 上调好的情绪模型换到 MI 就失效）泛化受限，这已是共识；近年的回应是大规模自监督预训练——LaBraM、BIOT、DMAE-EEG 等把不同数据集**统一成同一格式**喂给一个模型。EEGMoE 对这条路线的批评是：**统一格式只处理了「怎么喂」，没处理「喂进去之后域与域打架」的问题**。

论文的实证很直观（Fig. 1）：在经典 Transformer 上对 DEAP（ER）、BCIC4-2a（MI）、STEW（MWL）三个任务交替做自监督预训练，把每步梯度更新方向投影到 2-D 参数空间——ER 把参数往右下拉、MI 往左上拉、MWL 往右上拉。**异质域的梯度冲突是真实存在的**，而同质参数硬吃异构数据的后果是域特定细节被抹掉。

对 EEG 里已有的 MoE 工作，论文的批评分三类：IDMMOE、Seizure-MoE 用**全部专家加权求和**（丧失 MoE「选择性激活」的核心优势）；MoGE 是单任务有监督特征提取器；EEGMamba 虽有 MoE 但靠**任务 token 引导专家选择**、面向有监督多任务兼容，而非自监督的细粒度域解耦。EEGMoE 自称是**首个用 MoE 做解耦式 EEG 表征学习**的工作。

## 2 方法

### 2.1 数据预处理：4-D 脑地图输入

原始信号切 Ts 秒不重叠片段 → 每段分解为 **5 个频带**（δ 1–4Hz、θ 4–8Hz、α 8–14Hz、β 14–31Hz、γ 31–45Hz）→ 每个频带按电极的头皮位置摆成 **2-D 脑地图**（高斯平滑/z-score 消除突变）→ 沿频带堆成 3-D → 按时间堆成 4-D：X ∈ R^{(T×Sr)×B×H×W}。一个空间与频率编码器（两层 MLP，隐藏 64→128）沿通道和频带维度聚合，得到 embedding Z。注意这一步顺带解决了**跨数据集 montage 不一致**——所有数据集都被映射到统一的 2-D 电极网格上。

### 2.2 SSMoE 块：Specific + Shared 双专家组

域解耦编码器的 Transformer 层中，FFN 被替换为 SSMoE 块，由两部分相加：

**Specific MoE（Top-K 硬路由 → 域特定）**：E 个专家（每个是两层 MLP + GELU），路由器按 token 计算激活概率后只选 Top-K 个：

\[ g_x = W_e \cdot x, \qquad p_i(x) = \frac{\exp(g_{x_i})}{\sum_{j=1}^{|E|} \exp(g_{x_j})}, \qquad \mathrm{SpecMoE}(x) = \sum_{i \in \mathrm{TopK}} p_i(x)\, e_i(x) \]

**Shared MoE（软路由 → 域共享）**：F 个固定专家**无论输入是什么都全部参与**，保证共性表征不被路由丢弃：

\[ \mathrm{ShareMoE}(x) = \sum_{i \in F} p_i(x)\, f_i(x) \]

**SSMoE(x) = SpecMoE(x) + ShareMoE(x)**——简单相加。直觉分工：不同 token 按域挑选不同专家组合（特性），同一组共享专家对所有数据一视同仁地学习（共性）。

### 2.3 两阶段训练

**Stage 1 自监督预训练**：随机掩码 embedding，SSMoE 重构被掩表示，L1 重构损失 + **负载均衡辅助损失**（防 Top-K 路由把 token 都塞给少数过载专家）：

\[ \mathcal{L}_{\mathrm{pretrain}} = \mathcal{L}_1 + \alpha \mathcal{L}_{\mathrm{aux}}, \qquad \alpha = 1 \times 10^{-4} \]

**Stage 2 有监督微调**：继承预训练的域解耦编码器，接**单层线性分类头**，交叉熵微调。

## 架构图

![Figure 2 · EEGMoE 总体架构：4-D 预处理 → 空间/频率编码器 → 域解耦编码器（MHSA + SSMoE 块：Top-K Specific 专家组 + Soft Shared 专家组）](../assets/eegmoe-arch.png)

*Figure 2 · SSMoE 块细节：Specific Router 按 token 选 Top-K=2 个特定专家，Shared Router 让 2 个共享专家对所有 token 全程参与*

---

**相关阅读**

:material-arrow-right: [LUNA（拓扑统一路线，对照阅读）](luna.md) ｜ :material-arrow-left: [JET（流匹配生成）](jet.md) ｜ :material-grid-large: [通道适配与多任务学习](../topics/multi-task.md#channel-adaptation) ｜ :material-chart-box: [十一篇方法对比](../comparison.md) ｜ :material-home: [首页](../index.md)
