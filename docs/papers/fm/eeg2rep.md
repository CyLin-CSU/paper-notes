---
date: 2026-11-20
title: "EEG2Rep: Enhancing Self-supervised EEG Representation Through Informative Masked Inputs"
authors: [Navid Mohammadi Foumani, Geoffrey Mackellar, Soheila Ghane, Saad Irtza, Nam Nguyen, Mahsa Salehi]
venue: "KDD 2024"
year: 2024
tags: [EEG, 自监督, 掩码预训练, 表征学习, 隐空间预测]
status: "精读"
rating: 4
doi: "10.1145/3637528.3671600"
arxiv: "https://arxiv.org/abs/2402.17772"
code: "https://github.com/navidfoumani/eeg2rep"
one-liner: "Data2vec 式隐空间预测（预测完整输入的隐表示而非重构原始信号）+ SSP 语义保持掩码（决定保留谁而非掩码谁）+ VICReg 防坍缩；6 数据集 linear probing 全部第一，自预测系首次把 LP 拉起来"
---

# EEG2Rep: Enhancing Self-supervised EEG Representation Through Informative Masked Inputs

> **KDD 2024**（ACM SIGKDD，DOI 10.1145/3637528.3671600；arXiv 2402.17772）

**作者**：Navid Mohammadi Foumani, Geoffrey Mackellar, Soheila Ghane, Saad Irtza, Nam Nguyen, Mahsa Salehi（莫纳什大学 + Emotiv Research；与 Emotiv 合作完成，Driver Distraction 数据集来自其私有采集）

## 1 问题定位：自预测系为什么 linear probing 弱

论文把 EEG 自监督分成两族：**invariance 系**（SimCLR 式增强视图对比：TS-TCC、TF-C、SeqCLR）与**自预测系**（掩码重构：BENDR、MAEEG）。已有观察是自预测系的表示语义水平偏低——off-the-shelf 评测（linear probing）打不过 invariance 系。作者归因到 EEG 特有的三个挑战：

1. **低信噪比**：重构原始信号时，噪声直接主导重建损失——预测得再准也可能误差很大；
2. **幅值范围大**：被试间与电极摆放差异导致幅值量级不一，逐点回归原始值难优化；
3. **连续无显式分段**：EEG 不像文本有词、图像有 patch 的天然语义单元，掩码策略必须保证上下文里有足够语义供重构。

三个挑战对应三个解法：**隐空间预测**（在抽象表示空间重构，绕开噪声与幅值）、**表示归一化**（隐空间内量级统一）、**SSP 语义保持掩码**（决定保留谁）。

站内坐标：掩码策略轴上已有 REVE 时空块掩码（挖洞）、NeurIPT 幅度带掩码（挖哪条幅值）、TFM 频带掩码（挖频段），EEG2Rep 的 SSP 换了一个方向——**决定保留谁**，保证上下文是大块连续子序列。预训练目标轴上它是 EEG 里少见的数据2vec 式实现（预测目标 = 完整输入的 teacher 隐表示），介于 BIOT（BYOL 对齐，无显式预测头）与 REVE/BENDR（原始信号重构）之间。Kuruppu 批判综述「LP 落后 FT」的论断，本文是自预测系里的正面反例。

## 2 方法

### 2.1 三网络结构（Data2vec 式）

输入嵌入是 3 层 CNN：第一层深度可分离卷积捕捉通道间空间相关，随后线性空间滤波器提信噪比（神经信号在头皮上有固定空间分布、噪声分布更随机），max pooling + padding 出 patch 序列，加位置嵌入。

三个 transformer 网络：

- **Target network** \( \mathbf{y} = f_{\bar{\theta}}(S_x) \)（式 1）：吃**完整未掩码**输入，输出 patch 级表示作预测目标。表示做归一化——防坍缩、防高幅值主导目标特征。**目标块从 target encoder 的输出采样而非输入采样**：自注意力让每个目标 patch 已融合全部输入信息，语义水平因此足够高。
- **Context network** \( \mathbf{r}(q) = f_{\theta}(P_q) \)（式 2）：只处理 SSP 选出的可见 patch。
- **Predictor** \( \hat{\mathbf{y}}(i) = g_{\phi}(\mathbf{r}(q), m(i)) \)（式 3）：4 层 cross-attention transformer，mask token（共享可学习向量 + 位置嵌入）为 query，context encoder 输出为 key/value，对 \( M \) 个目标块各预测一次。

损失为预测块上的 L2（式 4）：\( Loss_{rec} = \frac{1}{M}\sum_{i}\sum_{j\in B_i}\|y_j - \hat{y}_j\|_2^2 \)，与 target 块重叠的 context 区域不计损失（防平凡解）。target 参数 \( \bar{\theta} \) 用 context 参数的 EMA 更新（式 5），\( \tau \) 从 \( \tau_0 \) 线性升到 \( \tau_e \)——早期更新频繁（context 还很随机）、后期放缓。

### 2.2 SSP：决定保留谁，而不是掩码谁

三种掩码的对比（原文 Figure 3，50% 掩码比例）：

- **随机掩码**（MAE 式）：无结构，大部分被掩点可由邻居插值平凡重构；
- **块掩码**（iBOT/Data2vec 式）：只管 mask 的结构，不保证剩下的可见区是连续语义段；
- **SSP**：反过来先决定**保留**谁——随机选 \( \beta \) 个起点对称扩展成块，块宽 \( \lceil (1-\rho)\times l/\beta \rceil \)（式 6），可见块允许重叠（实际保留量偏大），最后随机补单点把保留数凑到 \( (1-\rho)\times l \)。

效果：context encoder 每次看到的都是**大块连续子序列**，语义完整，逼 predictor 从语义上下文外推、而不是从插值取巧。消融（原文表 6）：多个掩码比例（10%–90%）× 多数据集，SSP 对随机掩码全面占优，且掩码比例越高优势越明显（比例越高，随机掩码的插值取巧越难、而 SSP 的上下文仍完整）。

### 2.3 效率与损失正则

**多掩码多预测**：\( N \) 个掩码视图共享同一个 target 表示（完整输入只过一次 target network，摊薄其开销），单次预测也覆盖多个目标块，重构损失更新为 \( Loss_{rec^*} = \frac{1}{M\times N}\sum_{q=1}^{N}\sum_{i=1}^{M}\sum_{j\in B_i}\|y_j-\hat{y}_j\|_2^2 \)（式 7）。

**VICReg 正则**：EMA + stop-gradient（BYOL/Data2vec/iBOT 式）防坍缩在实验中**不保证**学出高质量表示，于是加 VICReg 两项（式 8）：

\[
Total = \lambda\, Loss_{rec^*} + \mu\, v(R) + \gamma\, c(R)
\]

\( v(R) \) 是方差 hinge 损失（保 batch 内表示的多样性），\( c(R) \) 是协方差损失（惩罚表示各维相关，去冗余维度）。超参沿用 VICReg 原文设置。

## 3 实验与结果

**设置**：6 数据集两组——Emotiv 14 通道真实场景组（DREAMER 情绪、STEW 工作负荷、Crowdsourced 睁闭眼、Driver Distraction 私有集）+ TUH 临床组（TUAB、TUEV）。对比五个 SSL：invariance 系 TS-TCC / TF-C / BIOT，自预测系 BENDR / MAEEG。LP + FT 两协议，5 个随机种子报均值方差，单卡 A5000；每个数据集**各自自监督预训练**（无跨库大语料——见 §4 定位）。

**LP（原文表 2）**：EEG2Rep 六项全部第一——DREAMER 58.45（次优 BENDR 51.48）、Crowdsourced 81.66、STEW 69.04、Driver Distraction 76.88、TUAB 76.55、TUEV B-Acc 43.25。关键卖点：**自预测系首次在 LP 上全面压过 invariance 系**（BENDR/MAEEG 的 LP 明显弱于 TS-TCC/TF-C/BIOT，EEG2Rep 扭转）。

**FT（原文表 3）**：EEG2Rep（预训练版）同样六项第一——DREAMER 60.37、Crowdsourced 94.13、STEW 73.60、Driver Distraction 80.07、TUAB 80.52、TUEV B-Acc 52.95（BIOT 46.02、随机初始化版 44.25）。预训练 vs 随机初始化平均提升约 6%；AUROC 在 DREAMER 与 Driver Distraction 上分别 +5.81% / +2.26%。

**消融与附加**：组件消融（表 5，平均准确率 67.64%）；跨域预训练（表 4）——在 DREAMER 上预训练可提升相近活动构成的 STEW，但**全 Emotiv 数据集联合预训练没有超过域内预训练**，作者归因语料规模与被试覆盖不足，并指出需要更大的预训练数据集；噪声鲁棒实验（附录表 7：幅值缩放 0.5–2×、时移 ±50、DC 偏移 ±10、加性高斯 0–0.2）。

**规模与超参**（附录 B.1）：编码维 \( d_e = 16 \)、8 头、FFN ×4，输入嵌入 3 层卷积各 16 滤波器，batch 256，Adam 1e-3 余弦调度，预训练 500 epoch；**参数量原文未单列**（\( d_e=16 \) 属极小配置，与站内其他 FM 笔记的参数口径不可直接比）。注意：掩码比例的默认取值原文未在正文明确给出（消融表覆盖 10%–90%）。

## 4 定位与证据边界

- **不是跨库基础模型**：每个下游数据集各自做自监督预训练（500 epoch），没有 REVE/CBraMod 式的大语料预训练阶段。归入 fm 组是按「SSL 表征方法」口径；引用它当"基础模型"时要小心，它更接近"SSL 方法论 + Emotiv 场景验证"。
- **LP 反转的证据价值**：Kuruppu 综述与 EEGARENA 都记录了自预测系 LP 弱的通病；EEG2Rep 用"隐空间目标 + SSP + VICReg"三件套在 6 数据集上把 LP 拉到全面第一——这是「自预测系 LP 弱是方法性缺陷而非必然」的关键证据。但注意其预训练-评测都在同数据集内做，LP 反转是否在大语料跨库场景成立未验证。
- **d_e=16 的容量口径**：模型极小，六项第一的含金量要打折看——它证明的是目标函数设计（隐空间预测+SSP）在同等小容量下更优，不能外推成"EEG2Rep 架构优于大容量 FM"。
- 私有数据集 Driver Distraction 占六分之一评测面，不可复现。

---

**相关阅读**

:material-vector-link: [预训练范式对比（本文补上「隐空间预测 + 保留式掩码」两格）](../../topics/pretraining.md) ｜ :material-chart-box: [REVE（原始信号重构路线的对照面）](reve.md) ｜ :material-electric-bolt: [BIOT（BYOL 对齐路线，同场竞技的 invariance 系）](biot.md) ｜ :material-clipboard-check: [Kuruppu 批判综述（「LP 落后 FT」的出处，本文是其正面反例）](../reviews/kuruppu-critical-review.md) ｜ :material-atom: [NeurIPT（同期掩码策略另一方向：幅度感知挖洞）](neuript.md)
