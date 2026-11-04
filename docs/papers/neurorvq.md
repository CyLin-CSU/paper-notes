---
date: 2026-11-04
title: "NeuroRVQ: Multi-Scale Biosignal Tokenization for Generative Foundation Models"
authors: [Konstantinos Barmpas, Na Lee, Dimitrios Chalatsis, William Raftery, Yannis Panagakis, Dimitrios A. Adamos, Nikolaos Laskaris, Alexandros Koliousis, Dario Farina, Stefanos Zafeiriou]
venue: "arXiv 2025"
year: 2025
tags: [tokenization, RVQ, 多尺度卷积, 相位损失, 生物信号基础模型, EEG]
status: "精读"
rating: 4.5
arxiv: "https://arxiv.org/abs/2510.13068"
code: ""
one-liner: "4 个多尺度卷积分支 × 逐分支 RVQ(8192 码本 × 8/16 层)+ 圆周相位损失:同数据 EEG 重构 MSE 0.016 vs LaBraM 1.071(67 倍),5.9M 骨干在 EEG 五任务 mean BAcc 74.9(+4.2)、ECG 43 类 BAcc 58.33 较最强基线翻倍"
---
# NeuroRVQ: Multi-Scale Biosignal Tokenization for Generative Foundation Models

> **arXiv 2025**

**作者**:Konstantinos Barmpas, Na Lee, Dimitrios Chalatsis, William Raftery, Yannis Panagakis, Dimitrios A. Adamos, Nikolaos Laskaris, Alexandros Koliousis, Dario Farina, Stefanos Zafeiriou(帝国理工/Cogitat;通讯作者未标注)

## 1 问题定位:tokenizer 是 masked 建模的瓶颈

论文的出发点是 masked modeling 的成败取决于 tokenizer:现有两条路线都不行。深骨干/Transformer 式 tokenizer(如 CBraMod、BIOT)学出「纠缠冗余、不为重构优化」的表征,生成的 token 缺少 masked prediction 所需的保真度;码本路线(LaBraM 单码本 VQ、BrainOmni 单 RVQ)虽能学可重构的离散 token,但**都用单码本覆盖全频谱**,且训练损失不尊重重构目标的信号处理性质(最典型:对 ±π 边界不连续的相位角直接做 MSE)。结果是「codebook-based tokenizers with unfaithful signal reconstruction」。

生物信号侧的论证:EEG/ECG/EMG 共享「信息分布在多个频率尺度」的结构——EEG 有 delta–gamma 分频段节律,ECG 是低频 QRS 形态叠加高频细微成分,EMG 是运动单元募集(低频)与发放动力学(高频)的叠加。所以 tokenizer 的目标函数应当是**跨全部重要频率尺度的忠实重构**,而不是像 LaBraM 那样只保证粗粒度相似。三件套药方:多尺度架构 + 逐尺度 RVQ、相位感知损失、每模态一个极简 FM 来隔离「tokenizer 质量 → 下游性能」的因果链。这三味药是否各自起效,第 3 节消融逐一回头查账。

## 2 方法

### 2.1 总体:多尺度分支 + 逐分支 RVQ + Fourier 目标解码

输入 \( X \in \mathbb{R}^{C \times T} \) 切成 P 个长 w 的 patch(论文记作 \( x \in \mathbb{R}^{P \times w} \),通道维在记号里消失了——空间嵌入 SE 按电极索引,通道信息实际保留)。流程:多尺度时间编码器提特征 → 加共享时空嵌入过共享 Transformer → 每个尺度分支独立 RVQ 离散化 → 解码器以 Fourier 谱为目标重构。

多尺度时间编码器是 inception 式:S 个分支,每个分支 = 1D conv → GroupNorm(4 组/8 通道)→ GELU → pooling,**序列重复两次**。EEG/ECG(200 Hz)四分支卷积核 (21,15,9,5)→(9,7,5,3)——200 Hz 下最大感受野 105 ms 对齐低频形态、最小 15 ms 对齐快瞬态;EMG(1000 Hz)核 (51,17,8,5)→(25,9,4,3)。滤波器全部 8→8。输出 \( F_1,\dots,F_S \in \mathbb{R}^{w} \)。

时间嵌入 TE(按 patch 位置)与空间嵌入 SE(按电极在**预训练库全电极列表**中的位置,如 10-20 系统)维度均为 w,跨 S 个分支共享相加;共享 Transformer(12 层,并入 Dehghani et al. 2023/ViT-22B 的稳定性改造——具体内容未说明)输出多尺度 patch 表示 \( p_1,\dots,p_S \in \mathbb{R}^D \)。

### 2.2 逐分支 RVQ

每个时间分支配一套 RVQ 码本 \( R = \{V_i \mid i=1,\dots,N\} \),每层码本 \( V_i \in \mathbb{R}^{K \times D} \) 含 K=8192 个 D=128 维码字。量化逐层进行:

\[
z_1 = \arg\min_{v_1 \in V_1} \|\, \ell_2(p_1) - \ell_2(v_1) \,\|, \qquad p_{i+1} = p_i - z_i, \qquad \hat{p} = \sum_{i=1}^{N} z_i
\]

最终重构表示是 N 层选中码字之和。EEG/ECG 取 N=8、EMG 取 N=16(broadband 需要更大容量)。注意两处未披露:码本更新机制(EMA?死码重分配?)与 commitment 损失 \( \mathcal{L}_Q \) 的权重系数;另外隐藏维(表载 EEG/ECG 200)到码字维 128 之间的投影也没写。

### 2.3 相位感知损失:本篇最硬的技术贡献

解码器(3 层共享 Transformer)不直接重构原始波形,而是三个头分别预测 \( \log(1+\hat{A}) \)、\( \hat{c} \)、\( \hat{s} \)(幅值取对数压缩动态范围、相对强调高频)。相位为何要如此处理,Appendix A 给了三级递进:

1. 原始相位 MSE 在 ±π 边界不连续:\( \hat{\varphi}=\pi-\epsilon,\ \varphi=-\pi+\epsilon \) 时损失 \( \approx 4\pi^2 \),几乎相同的角却产生爆炸梯度(LaBraM 正是这么做的);
2. 改用 sin/cos 表示得 \( \mathcal{L}_{r} = 2 - 2\cos(\hat{\varphi}-\varphi) \),连续了,但当 \( \hat{\varphi} \approx \varphi \pm \pi \)(预测最大错)时梯度 \( 2\sin(\hat{\varphi}-\varphi) \approx 0 \)——**最错的预测反而收不到学习信号**;
3. 所以让网络直接预测二维向量 \( (\hat{c}, \hat{s}) \),与目标 \( (\cos\varphi, \sin\varphi) \) 做余弦相似度做方向对齐:最大错误产生大梯度,且 ĉ/ŝ 联合优化而非独立两个量。tanh 输出把范数压在 \( \le\sqrt{2} \),实践中预测范数自然趋近 1。

总目标(式 6):

\[
\mathcal{L}_T = \underbrace{\sum_i \| \log(1+\hat{A}_i) - \log(1+A_i) \|_2^2}_{\text{对数幅值}} + \underbrace{1 - \sum_i \frac{\hat{c}_i \cos\varphi_i + \hat{s}_i \sin\varphi_i}{\sqrt{\hat{c}_i^2 + \hat{s}_i^2}}}_{\text{相位}} + \underbrace{\| \hat{X}_i - X_i \|_2^2}_{\text{时域正则}} + \mathcal{L}_Q
\]

时域项的立场值得注意:LaBraM 说直接重构原始波形不稳定所以回避,本文的实验结论是**加上**时域 MSE 反而提供稳定梯度、让相位项充分发挥(Appendix B 的协同分析)。可选的单位圆正则 \( \mathcal{L}_{reg} = \lambda_{circle} \sum_i (\hat{c}_i^2 + \hat{s}_i^2 - 1)^2 \) 的敏感性分析(Table 3)显示 λ=0.0 的 MSE 最低(EEG 0.035 vs λ=0.1 的 0.050,劣化 43%),主结果却保守保留 λ=0.1——论文称之为 "negligible cost",这个措辞与自家表格有出入。

### 2.4 Scaling 分析与模态自适应

四个设计旋钮(patch 长 w、分支数 S、卷积核组、RVQ 深度 N)各自对准模态的谱时特性。S∈{1,2,4} × N∈{1,...,32} 的系统 scaling(小数据集上 50 epoch:EEG 用 PhysioNet MI、ECG 用 PTB、EMG 用 emg2pose-small):加深码本收益最大;加分支在小 N 时补益明显(各频段单独量化更容易);ECG(信号最刻板)最早饱和,EEG 持续受益于加深,EMG 最吃深度。最终按算力取 S=4、N=8/8/16。

### 2.5 NeuroRVQ-FM:刻意简单的下游验证

FM 复用同一多尺度编码器 + Transformer + token 预测头,以对称掩码策略(LaBraM 式)0.5 比例做 masked-token 预训练(50 epoch、bs 64、AdamW 5e-4),下游接分类头全微调——「刻意保持架构简单以隔离 tokenizer 的贡献」。正文没有说明 FM 输入到底是量化后的离散 token 还是编码器连续 embedding,只有一句 "operates on the tokenized representation"。FM 预训练语料与 tokenizer 相同,总量(小时数)未披露。

## 架构图

![Figure 1 · NeuroRVQ tokenizer:多尺度时间编码器 → 共享嵌入 → Transformer → 逐分支 RVQ → Fourier 目标解码](../assets/neurorvq-framework.png)

*Figure 1 · 下行为主干:Input Biosignal Patches → Multi-Scale Temporal Encoder(S 个分支)→ Transformer Encoder → 多尺度 patch 表示 p1..pS → Lookup operation 进 RVQ Codebooks → Tokenizer Decoder → Reconstructed Patches;上行为放大细节:S 个 Temporal Branch 输出 F1..FS,与 Shared Temporal/Spatial Embeddings 相加成 Combined Embeddings;右侧 RVQ 放大:每分支 R1..RN 各含 V1..VK 个码字。图中只画了架构,损失三项(对数幅值/相位/时域)不在图内*

---

**相关阅读**

:material-vector-link: [Tokenization 演进(RVQ/多尺度缺口由本篇填补)](../topics/tokenization.md) ｜ :material-vector-circle: [BrainRVQ(RVQ 分支后续:双域 + 层间自回归)](brainrvq.md) ｜ :material-tag: [LaBraM(被对照 67× 的单码本 VQ 前作)](labram.md) ｜ :material-vector-polyline: [TFM-Tokenizer(token 作输入的分岔路线)](tfm-tokenizer.md) ｜ :material-compare: [CBraMod(深骨干 tokenizer 的批评对象)](cbramod.md) ｜ :material-heart-pulse: [BIOT(连续 patch 路线的崩盘基线)](biot.md) ｜ :material-home: [首页](../index.md)
