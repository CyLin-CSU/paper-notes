---
date: 2026-11-06
title: "Uni-NTFM: A Unified Foundation Model for EEG Signal Representation Learning"
authors: [Zhisheng Chen, Yingwei Zhang, Qizhen Lan, Tianyu Liu, Huacan Wang, Yi Ding, Ziyu Jia, Ronghao Chen, Kun Wang, Xinliang Zhou]
venue: "ICLR 2026"
year: 2026
tags: [EEG, 时频融合, 交叉注意力, 拓扑嵌入, MoE, 掩码预训练]
status: "精读"
arxiv: "https://arxiv.org/abs/2509.24222"
code: "https://github.com/Zhisheng-researcher/Uni-NTFM"
one-liner: "逐电极提取时域与频带功率特征，双向交叉注意力融合，再以拓扑嵌入和 MoE Transformer 学习 EEG 表示"
---

# Uni-NTFM: A Unified Foundation Model for EEG Signal Representation Learning

> **ICLR 2026** · [会议论文](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b16e55ac49f93d33a4b87747d5121b64-Abstract-Conference.html) · [arXiv v2 全文](https://arxiv.org/html/2509.24222v2) · [作者代码](https://github.com/Zhisheng-researcher/Uni-NTFM)

**作者**　Zhisheng Chen, Yingwei Zhang, Qizhen Lan, Tianyu Liu, Huacan Wang, Yi Ding, Ziyu Jia, Ronghao Chen, Kun Wang, Xinliang Zhou

## 1 问题定位

波形形态、频带功率和电极布局是同一段 EEG 的不同信息。Uni-NTFM 先分路处理波形与频带功率，再让两路特征相互查询。融合后，模型用分层位置嵌入区分电极，用混合专家 Transformer 处理电极序列。[原文 §1、图 2](https://arxiv.org/html/2509.24222v2#S2.F2)

## 2 方法

### 2.1 每个电极的整段信号生成一个 token

输入组织为 \(\mathbb R^{B\times R\times E\times T}\)。\(R\) 是预定义区域数，\(E\) 是每区的电极槽数，\(T\) 是单段波形的采样点数。论文在输入片段内以**整段单电极波形**为投影单元，因此注意力序列长度由电极槽数决定。作为对照，[REVE](reve.md) 会把每个电极的同一段波形沿时间再切成多个 patch。论文报告 200 Hz 预处理，表 8 列出序列长度 1600 和五个频带。[原文 §2.1–2.2、§3.1、表 8](https://arxiv.org/html/2509.24222v2#A7.T8)

| 路径 | 每个电极如何生成特征 | 去向 |
| --- | --- | --- |
| 时域路径 | 一维卷积提取波形特征 \(h_T\) | 进入双域交叉注意力 |
| 频域路径 | 对整段做 DFT，对各频带内的谱功率取均值，再用 MLP 投影为 \(h_F\) | 进入双域交叉注意力，同时提供频域重建目标 |
| 原始信号路径 | 对波形另做标准投影得到 \(h_R\) | 按论文定义，加到融合特征上，同时提供时域重建目标 |

频域路径在注意力前已把各频带功率投影成**每个电极一个向量**。该向量描述整段功率分布，输入粒度与 [TFM-Tokenizer](tfm-tokenizer.md) 中保留时间窗和频率块的 STFT 表示不同。[原文 §2.2.1–2.2.3、附录 E.1](https://arxiv.org/html/2509.24222v2#S2.SS2)

### 2.2 双域交叉注意力

双域交叉注意力模块（Dual-domain Cross-attention Module，DCM）做两次查询。下式对应原文公式 (5)–(6)。时域序列从频域序列读取信息，频域序列也从时域序列读取信息。

\[
\begin{aligned}
H'_T &= \operatorname{LN}\!\left(H_T+\operatorname{CrossAttn}(H_T,H_F,H_F)\right),\\
H'_F &= \operatorname{LN}\!\left(H_F+\operatorname{CrossAttn}(H_F,H_T,H_T)\right).
\end{aligned}
\]

交叉注意力的三个输入依次为 \(Q,K,V\)。模型将两路结果拼接，再用前馈网络映射回主干宽度。**这里的频域 Key 对应电极级频域向量**，所以 \(H_T\) 查询的是不同电极的频域表示，注意力权重本身无法按 \(\alpha\)、\(\beta\) 等频带直接解读。[原文 §2.2.4、式 (5)–(6)](https://arxiv.org/html/2509.24222v2#S2.SS2.SSS4)

### 2.3 三层拓扑嵌入

拓扑嵌入（Topological Embedding，TE）将电极分到额、中央、颞、顶和枕五个区域。每个电极槽加入所属区域、区域内位置和全局位置的三种可学习向量。论文将三者与交叉注意力输出及原始信号投影相加，再把结果送入主干。Uni-NTFM 用模板索引查找嵌入，REVE 从电极三维坐标和时间索引计算位置向量。[原文 §2.3、式 (7)、附录 E.2](https://arxiv.org/html/2509.24222v2#S2.SS3)

### 2.4 MoE Transformer

主干对电极 token 做多头自注意力，在查询和键上用旋转位置编码（RoPE）。每层的前馈部分采用混合专家（Mixture of Experts，MoE）。路由器给每个 token 选取得分最高的 \(k\) 个专家，按门控权重组合输出，并用负载均衡辅助损失约束专家用量。论文给出的四档总参数量为 57M、427M、912M、1.9B。[原文 §2.4、表 8](https://arxiv.org/html/2509.24222v2#S2.SS4)

### 2.5 双域掩码重建

论文在输入特征序列上选出掩码位置，用可学习的 mask embedding 替换。主干输出接两个重建头，分别拟合原始信号路径的投影 \(h_R\) 和频域路径的投影 \(h_F\)。两个重建项在被掩位置计算均方误差，再加上 MoE 的负载均衡项。表 8 报告重建项的时域与频域权重为 0.8 和 0.2，掩码比例为 0.25。

这里的监督空间是**两类投影特征**。论文公式没有要求两个解码输出在同一张局部 STFT 图逐点对齐。预训练语料约 28,000 小时、九个数据集、逾 17,000 名被试。下游分别考察冻结主干的线性探针和全量微调。[原文 §2.5、§3.1–3.3、表 8](https://arxiv.org/html/2509.24222v2#S2.SS5)

## 3 关键设计

**区分频带特征和频带 token。** Uni-NTFM 已将时域查询用于频域特征。若要研究同一个波形窗如何选择不同频率块，需要沿频率轴保留多个 Key/Value，并将查询与谱帧的时间支持对齐。对照时应保持可用频谱和主干 token 数一致，以区分交叉注意力的作用与新增谱输入的作用。[原文 §2.2.2–2.2.4](https://arxiv.org/html/2509.24222v2#S2.SS2)

**复现时核对公开实现与论文公式。** 作者仓库说明只提供部分实现。当前代码在两次交叉注意力中使用形状为 \([B,L,D]\) 的电极序列，反向查询读取已更新的时域序列。公开前向先执行电极间融合，再替换被掩 token。因此若沿用该前向做严格的通道遮挡实验，应检查被掩电极的信息是否先经融合流入可见 token。这项检查针对公开代码的数据流，论文实验使用的完整训练实现仍待核实。[交叉注意力代码](https://github.com/Zhisheng-researcher/Uni-NTFM/blob/main/model.py#L284-L307) · [前向与掩码](https://github.com/Zhisheng-researcher/Uni-NTFM/blob/main/model.py#L635-L669)
