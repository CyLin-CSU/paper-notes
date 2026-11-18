---
date: 2026-11-18
title: "Representation Learning and Foundation Models for Electroencephalography Analyses"
authors: [Zhe Sage Chen, Bao-Liang Lu, Wei Wu]
venue: "IEEE Signal Processing Magazine 2025"
year: 2025
tags: [综述, 表示学习, 迁移学习, 词元化, 基础模型, EEG-to-Content]
status: "精读"
rating: 4
arxiv: "https://doi.org/10.1109/MSP.2025.3595320"
code: ""
one-liner: "信号处理杂志视角的 EEG FM 全景：19 个模型按词元化/嵌入/位置编码/骨干/损失逐项拆表，外加迁移学习四类地图与三个落地案例"
---

# Representation Learning and Foundation Models for Electroencephalography Analyses

> **IEEE Signal Processing Magazine, 2025 年 9 月 · 专刊「Accelerating Brain Discovery Through Data Science and Neurotechnology」**

**作者**：Zhe Sage Chen（NYU，精神病学与神经科学）、Bao-Liang Lu（上海交大）、Wei Wu

## 1 问题定位

与前两篇纯 ML 视角的综述不同，这篇从**信号处理传统**出发：先铺 EEG 信号处理基础（谱分析、时空分析、源定位、功能连接、非线性分析）与图/流形方法（图傅里叶变换、黎曼几何协方差），再进入表示学习原理（「任务相关特征 + 上下文无关特征」的分解式），最后落到 FM。覆盖 EEG 与 iEEG，系统检索窗口 2020-01–2025-06，选出 19 个模型列表。

## 2 FM 拆解表：目前最细的一张

Table 1 + Figure 2 把 19 个模型（BENDR、BIOT、BrainBERT、BrainWave、Brant、Brant-2、CBraMod、EEGFormer、EEGPT、FEMBA、FoME、Gram、LaBraM、MENTALITY、MMM、Neuro-BERT、Neuro-GPT、NeuroLM 等）按七个字段逐项拆开：词元化 / 输入嵌入 / 位置编码 / 骨干 / 预训练损失 / 参数量 / 是否开源。

**词元化五类 + 一个附加项**：

| 词元化 | 代表 |
|---|---|
| 时域 patching（主流） | BIOT、Brant 系、CBraMod、EEGPT、FoME、Gram、LaBraM、NeuroLM 等 |
| 频域 patching | EEGFormer（FFT 后按谱切段） |
| 时频 patching | BrainBERT、BrainWave（先做 2D 谱图再切） |
| 空时 2D patching | FEMBA（通道 × 时间二维块） |
| 微分熵特征 | MMM |
| （附加）VQ 量化 | EEGFormer、Gram、LaBraM、NeuroLM |

值得记的两个 trade-off：patching 让长记录在算力上可行，但**切段边界会破坏细粒度时序模式**——BENDR 因此不走 patching，用卷积编码器直接对原始信号降采样；BrainBERT 则在切段前先做 superlet 变换取时频分辨率。VQ 的动机是连续分布难处理多模态，量化到码本「捕捉反复出现的模式」。

其余字段也有现成结论：位置编码序列序可学习（LaBraM、FoME）vs 固定正弦（BIOT、BrainBERT、Gram），空间 PE 可学习（BIOT、LaBraM）vs 固定（Gram、MMM）；骨干分 encoder-only（多数）/ decoder-only 自回归（EEGPT、Neuro-GPT、NeuroLM）/ encoder-decoder（EEGFormer、Gram、MMM）；损失按目标配——MSE 重构、交叉熵（预测离散码字）、对比损失（BENDR、BIOT）。自回归模型的时序由因果结构隐含，不另加 PE。

**表内勘误**（站内核对）：FoME 年份印成 2021（应 2024）；表中 EEGPT 条目是 decoder 自回归、1–1090M 参数，实为站内 [BrainGPT](../fm/braingpt.md)（Yue et al.）而非站内 [EEGPT](../fm/eegpt.md)（Wang et al.）；BENDR 架构一栏「wav2dec」为笔误。

## 3 迁移学习与不变表示

独立成章，可当下游适配的路线图。域偏移按四轴分：跨被试 / 跨会话 / 跨设备 / 跨任务。方法按四类分：instance-based（重加权、样本选择）、feature-based（黎曼流形对齐、CSP 改造、预训练特征）、model-based（微调预训练网络）、classifier-based（域对抗 DANN、集成投票）。不变表示三条路：对比学习、对抗推断、因子化 VAE 解耦「共性内容 / 被试风格」。

## 4 三个落地案例

- **SELSER**（抑郁生物标志物）：空间滤波 + 频带功率 + 线性回归在稀疏潜空间里全局最优求解，预测舍曲林疗效 HAMD 变化 r=0.6（p=5.19×10⁻¹¹）；同一模型放到安慰剂臂 r=−0.03——阴性对照做得很干净。
- **Brant-X**（多模态对齐）：冻结 Brant-2（预训练 4 TB+ EEG）作 EEG 端，EXG 端新训编码器，patch 级 + 序列级两级对比对齐；任务跨睡眠分期（EEG+EOG）、情绪（EEG+ECG）、冻结步态（EEG+EMG）。
- **NeuroLM**（多任务指令微调）：VQ 词元器 + LLM 因果建模 + 多任务指令微调，预训练 25 000 h，单模型跨六任务推理。

## 5 规模、可解释性与开放科学

Scaling 证据：LaBraM 的模型/数据双缩放实验；非侵入语音解码单被试 175 h→48% vs 10 h→2.5% top-1，作者预期 FM 性能随 10 000 h 量级语料继续提升。可解释性一节 beyond attention：归因分析（积分梯度、SHAP）、概念激活向量、因果表示学习的可辨识性定理、白盒 energy transformer。数据一节给了公开语料库清单（Harvard 28 万+ 记录、UCSD NEMAR 2.7 万被试等）并点名地理/性别/年龄偏置。收尾直言「Can foundation models be the ultimate panacea? Probably not.」

## 6 站内视角

- Table 1 的词元化五分类是本站 [Tokenization 演进专题](../../topics/tokenization.md) 之外**轴最接近的现成对照**：它按「切段几何」分类，站内按「词表怎么来、用在哪」，写词元化节时先引后立。
- TL 四分类与本站 REVE 微调策略（缓存线性探针 → 小学习率微调）同属 model-based 一支，可直接引用其框架。
- 与同期 [Kuruppu 批判性综述](kuruppu-critical-review.md) 相比，这篇更全景、批判更轻（「独立验证仍缺」一句带过）。

---

**相关阅读**

:material-call_split: [Tokenization 演进专题（与 Table 1 五分类对照）](../../topics/tokenization.md) ｜ :material-link-variant: [LaBraM（Table 1 中 VQ 谱预测一支）](../fm/labram.md) ｜ :material-tag-multiple: [NeuroLM（EEG-文本对齐 + 指令微调案例）](../fm/neurolm.md) ｜ :material-magnify-remove-outline: [EEGPT（注意与表中条目同名不同人）](../fm/eegpt.md) ｜ :material-clipboard-check: [Kuruppu 批判性综述（同期更严的对照）](kuruppu-critical-review.md) ｜ :material-home: [首页](../../index.md)
