---
date: 2026-11-19
title: "NeurIPT: Foundation Model for Neural Interfaces"
authors: [Zitao Fang, Chenxuan Li, Hongting Zhou, Shuyang Yu, Guodong Du, Ashwaq Qasem, Yang Lu, Jing Li, Junsong Zhang, Sim Kuan Goh]
venue: "arXiv 2025"
year: 2025
tags: [EEG, 基础模型, 掩码预训练, MoE, 电极坐标编码, 脑区分组]
status: "精读"
rating: 3.5
arxiv: "https://arxiv.org/abs/2510.16548"
code: ""
one-liner: "幅度感知掩码（按幅值带挖洞防插值）+ 专家数随深度递增的 PMoE + 3D 电极坐标嵌入与脑区分组池化；8 个 BCI 下游多数 B-ACC 第一，增益集中在低资源与类不平衡端"
---
# NeurIPT: Foundation Model for Neural Interfaces

> **arXiv 2025**

**作者**：Zitao Fang, Chenxuan Li, Hongting Zhou, Shuyang Yu, Guodong Du, Ashwaq Qasem, Yang Lu, Jing Li, Junsong Zhang, Sim Kuan Goh（厦门大学马来西亚分校为主，含 Columbia、香港理工、厦门大学、哈工大深圳；通讯 Junsong Zhang、Sim Kuan Goh）

## 1 问题定位：随机掩码在时序里退化成插值

论文接的是 EEG 基础模型的三个常规难题：被试间/任务间/记录条件间变异大、电极配置不统一、下游任务异构。方法上的切入点只有一个具体批评——**随机掩码在时间序列上容易退化为局部插值**：相邻采样点高度相关，被挖掉的点靠两侧邻居平均就能猜个八九不离十，重建损失降了但表示没学到结构。这个批评在时序预训练文献里有出处（论文引 [24]），站内的掩码线也已经在往同一个方向走：REVE 用时空连续块掩码、TFM-Tokenizer 用频带掩码，都是"结构化掩码优于随机"。NeurIPT 把结构化的轴换成了**幅值**——挖掉特定幅值带，插值取巧失效。第二个切入点是容量：EEG 混着频段差异、瞬态事件和伪迹，单一 FFN 分不开，于是把 MoE 引进主模型。

站内坐标：CBraMod 的十字交叉注意力、REVE 的块掩码解决了"时空怎么注意、怎么挖洞"，NeurIPT 补的是"挖哪里"和"FFN 换不换"这两格；通道适配一格用 3D 坐标编码，与 LUNA 的可学习 query 统一、REVE 的 4D 傅里叶编码同题不同解。

## 2 方法

### 2.1 输入：单点 token + 3D 电极嵌入

不切 patch——每个时间点 × 每个通道是一个 token（Crossformer 式），\( s_{t,d} = \mathbf{E}x_{t,d} + PE^{(t)} + PE^{(s)} \)。作者给的理由是保留逐点细节、利于捕捉尖峰；层级合并（见 2.3）负责把序列长度降下来。空间编码用每个电极的 3D 坐标 \((x_d, y_d, z_d)\)，三个轴各自做正弦编码（每轴 \( d_{model}/3 \) 维）再拼接，与正弦时间编码相加。T 和 D 都可变，换电极系统不用改结构、不用补零（对比 EEGPT / CBraMod 的固定通道处理）。

预训练与下游的通道口径都是 double-banana 双极 20 通道——3D 坐标作用在双极通道上，论文未说明双极通道的坐标如何定义（未披露项）。

### 2.2 AAMP：按幅值带掩码

对每个通道 \( d \)：把该通道 \( T \) 个采样点按幅值排序，随机取分位数 \( \xi_d \sim \mathcal{U}(0,1) \)，以排序后第 \( \xi_d T \) 个点为中心取一段覆盖 \( P \cdot T \) 个点的**幅值区间** \([\mathcal{L}_d, \mathcal{U}_d]\)，落进区间的点全部掩码。\( P \) 在 \{20%, 35%, 50%\} 中动态取（表 13）。被掩位置按 BERT 式 80/10/10 处理：80% 换 [mask] token、10% 换随机 embedding、10% 保留。encoder 只处理未掩码点（掩码位置的注意力分数置零），decoder 用 [mask] token 重构，损失为 \( \ell_p \) 范数（式 7）。

机制上是把"挖哪里"从空间位置换到幅值分布：被挖掉的是一段特定幅值的点（可能全是波峰，也可能全是低幅段），两侧邻居插不出它们。附录 B 的消融：小模型（\( d_{model}=256 \)）+ SVM 探针（TUEV）下，AAMP 比随机掩码高 **5.25%**；论文同时报告随机掩码的重构训练损失更低——说明幅度掩码是更难的重构任务，损失低不等于表示好。

### 2.3 骨干：Crossformer TSA + 渐进式 MoE

骨干是改造版 Crossformer：每个 encoder 层先做跨时间注意力（每个通道一条序列，所有通道共享 MSA），再做跨维度注意力（每个时间步一条序列），Pre-LN、SwiGLU、FlashAttention-2。第 1 层之后每层用可学习合并矩阵把相邻 \( m_l \) 个 token 合并成粗粒度段（合并层数 [1,4,1,2,1,2]，表 13），序列长度逐层下降。

FFN 换成 **PMoE**：token 级 TopKSoftmax 路由（top 0.5%），每个专家是 hidden 512 的私有 FFN，另有一个 hidden 768 的共享专家始终参与（式 9），配 importance + load-balance 辅助损失（权重 0.8，式 24）。"渐进"指专家数随深度递增——encoder 六层的专家数 [0,2,2,4,4,6]：前两层不带专家，越深专家越多，共享专家负责共性、深层专家分工特异特征。decoder 无专家。消融（表 3）：递增配置 TUEV 68.94%，对无专家 65.83%、均匀 [4,4,4,4,4,4] 65.91%、递减 [6,4,4,4,0,0] 65.80%；换其他递增配置（表 4）结果接近，作者的解释是收益来自"随深度递增"这个策略本身。

### 2.4 下游读出：脑叶内池化 + 脑叶间拼接

IILP 只在微调期用：encoder 各层输出先沿时间均值池化得每通道向量，再把通道按脑叶分组（额、左颞、右颞、顶、枕）做组内平均，各脑叶向量拼接（式 12–13），最后把全部 encoder 层的拼接结果再拼接（式 14）进 MLP 分类头。动机是抑制同脑区通道冗余、保留脑叶间判别信息。消融（表 5）：对无池化、均值池化、半球、冠状、矢状分组，IILP 在 TUEV / MentalArithmetic / Mumtaz2016 / SEED-V / BCIC-IV-2A 五个数据集同时最好（BCIC-IV-2A 55.04%，均值池化只有 37.24%）。类不平衡下游用 logit 调整的 Bal-BCE 损失（式 25）。

一个值得记录的细节：SEED-V 和 BCIC-IV-2A 微调时验证集性能早饱和，作者的处理是**把预训练权重重新随机初始化**再训，理由是"预训练表征与目标任务失配"（§D.1）——预训练在这两个任务上是负资产。

## 3 预训练设置与规模

14 个公开数据集、共 2000+ 小时，显式排除全部 8 个下游数据集。预处理沿 CBraMod：短于 5 分钟的记录剔除、每段掐头去尾各 1 分钟、double-banana 双极 20 通道。输入取 256 个采样点。约 400K 步、40 epoch、有效 batch 480（表 13 单卡 60 × 8 卡）、AdamW 峰值 3e-4 + OneCycle、bf16，8×RTX 4090 共约 30 小时（§D.1）——同属"EEG 基础模型预训练算力门槛不高"的例证（对照 REVE 单次 Base 约 260 A100·GPU 小时）。

参数量：**73.5M（激活参数）**，原文表 16 口径；总参数未单列。与表 16 其他条目对比时注意口径一致（该表给 CBraMod 4.2M、LaBraM-Base 5.8M，均为各自论文口径）。

低资源（附录 B 表 12）：10% 下游标注量保持 80–90% 性能，1% 保持 64–80%。

## 4 下游结果与证据边界

8 个下游任务全部按 CBraMod 协议（表 1、表 2，B-ACC）：

| 数据集 | 最佳基线（B-ACC） | NeurIPT | 差 |
|---|---|---|---|
| MentalArithmetic | CBraMod 72.56 | **86.46** | +13.90 |
| Mumtaz2016 | CBraMod 95.60 | **98.03** | +2.43 |
| PhysioNetP300 | EEGPT 65.02 | **67.31** | +2.29 |
| Sleep-EDFx | EEGPT 69.17 | **70.47** | +1.30 |
| SEED-V | CBraMod 40.91 | **41.04** | +0.13 |
| BCIC-IV-2A | CBraMod 51.38 | **55.04** | +3.66 |
| TUAB | CBraMod 82.89 | **82.93** | +0.04 |
| TUEV | CBraMod 66.71 | **67.61** | +0.90 |

两点证据边界：TUAB 上 Cohen's Kappa（−2.18）与加权 F1（−2.78）输给 CBraMod，论文正文承认；组件消融（表 6、表 7）用的是**从零训练**的模型（作者注明因预训练耗时跳过预训练阶段），结论不能直接外推到完整预训练模型。增益的分布规律：低资源、类不平衡、通道覆盖全的任务收益大（MentalArithmetic +13.90），大样本临床任务（TUAB / TUEV / SEED-V）与 CBraMod 打平。

## 架构图

![Figure 3 · NeurIPT 总体框架：EEG 经 3D 电极嵌入进入 N 层 TSA encoder（时间注意力 + 空间注意力，FFN 换成渐进式 PMoE，Block 1 两个专家、Block N \(n+1\) 个专家加共享专家）；预训练走 (N+1) 层 decoder 重构被幅度掩码挖掉的信号点（\( \mathcal{L}_{AAMP} \)），下游用脑叶内池化 + 脑叶间拼接（Frontal / Occipital / Temporal L / Temporal R / Parietal）出类别](../../assets/neuript-framework.png)

*Figure 3 · 原文图内专家画为羊驼形象、共享专家为戴礼帽形象，仅为示意画风*

---

**相关阅读**

:material-vector-link: [预训练范式对比（站内主线，本文补上「按幅值掩码」一格）](../../topics/pretraining.md) ｜ :material-chart-box: [REVE（时空块掩码 + 4D 坐标编码）](reve.md) ｜ :material-timeline: [CBraMod（同款预处理协议与十字交叉骨干）](cbramod.md) ｜ :material-layers: [EEGMoE（特殊/共享双专家，本文改为深度递增）](eegmoe.md) ｜ :material-code-json: [LUNA（同题不同解的通道适配：query 统一 vs 3D 坐标）](luna.md)
