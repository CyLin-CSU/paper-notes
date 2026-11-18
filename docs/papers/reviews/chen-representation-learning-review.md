---
date: 2026-11-18
title: "Representation Learning and Foundation Models for Electroencephalography Analyses"
authors: [Zhe Sage Chen, Bao-Liang Lu, Wei Wu]
venue: "IEEE Signal Processing Magazine 2025"
year: 2025
tags: [综述, 表示学习, 迁移学习, 词元化, 基础模型, EEG-to-Content]
status: "精读"
rating: 4
doi: "10.1109/MSP.2025.3595320"
arxiv: ""
code: ""
one-liner: "信号处理杂志视角的 EEG FM 全景：18 个模型按词元化/嵌入/位置编码/骨干/损失逐项拆表，外加迁移学习四类地图与三个落地案例"
---

# Representation Learning and Foundation Models for Electroencephalography Analyses

> **IEEE Signal Processing Magazine, 2025 年 9 月 · 专刊「Accelerating Brain Discovery Through Data Science and Neurotechnology」**

**作者**：Zhe Sage Chen（NYU，精神病学与神经科学）、Bao-Liang Lu（上海交大）、Wei Wu

## 1 问题定位

与前两篇纯 ML 视角的综述不同，这篇从**信号处理传统**出发：先铺 EEG 信号处理基础（谱分析、时空分析、源定位、功能连接、非线性分析）与图/流形方法（图傅里叶变换、黎曼几何协方差），再进入表示学习原理（「任务相关特征 + 上下文无关特征」的分解式），最后落到 FM。覆盖 EEG 与 iEEG，系统检索窗口 2020-01–2025-06，选出 18 个模型（原文文字称 19，按其 Table 1 行数为 18）。

## 2 FM 拆解总表（原 Table 1 复现）

18 个模型按七个字段逐项拆开。「—」为原文 N/A 或未报；站内命名换算：表中 EEGPT（decoder 自回归条目）= 站内 [BrainGPT](../fm/braingpt.md)，Mentality = MENTALITY。

| 模型 | 词元化 | 输入嵌入 | 位置编码 | 骨干 | 预训练损失 | 参数量 | 开源 | 年份 |
|---|---|---|---|---|---|---|---|---|
| BENDR | 无切段（卷积编码器） | 时序映射 | 时间（可学习） | 时序 Transformer encoder | 掩码信号重构 + 对比损失 | — | ✅ | 2021 |
| BIOT | 时域切段 | 谱映射 | 序列（固定）+ 空间（可学习） | 线性时空 Transformer encoder | 扰动重构对比损失 | 3M | ✅ | 2023 |
| BrainBERT | 时频切段 | z-score 归一化 | 序列（固定） | 时空 Transformer encoder | 内容感知 MAE（谱图重构） | 43M | ✅ | 2023 |
| BrainWave | 时频切段 | 谱时映射 | 序列（可学习） | 时序+空间 Transformer encoders | MSE 掩码重构 | — | ✗ | 2024 |
| Brant | 时域切段 | 时序+谱映射 | 序列（可学习） | 时序+空间 Transformer encoders | MSE 掩码重构 | 68–505M | ✅ | 2023 |
| Brant-2 | 时域切段 | 时序+谱映射 | 序列（可学习） | 时序+空间 Transformer encoders | MSE 掩码重构 + 预测 | 115–1065M | ✅ | 2024 |
| CBraMod | 时域切段 | 时序+谱映射 | 空间+序列（可学习） | 时序+空间 Transformer encoders | MSE 掩码重构 | — | ✅ | 2025 |
| EEGFormer | 频域切段 + VQ | 谱映射 | 序列（可学习） | 时序 Transformer enc–dec | MSE 信号重构 | — | ✅ | 2024 |
| EEGPT（=站内 BrainGPT） | 时域切段 | 无 | 空间（可学习） | 时序 Transformer decoder | MSE 自回归预测 | 1–1090M | ✅ | 2025 |
| FEMBA | 空时二维切段 | 时空映射 | 序列（可学习） | Mamba encoder + 轻量 decoder | Smooth-MAE 掩码重构 | 8–389M | ✗ | 2025 |
| FoME | 时域切段 | 时序+谱映射 | 序列（可学习） | 时序+空间 Transformer encoders | MSE 掩码重构 | 745M | ✅ | 2021（勘误：应 2024） |
| Gram | 时域切段 + VQ | 时序映射 | 空间+序列（全固定） | 时空 Transformer enc–dec | 谱重构 MSE + 掩码基类 CE | 6–251M | ✅ | 2025 |
| LaBraM | 时域切段 + VQ | 时序映射 | 空间+序列（全可学习） | 时空 Transformer encoder | 掩码码字预测 CE | 5–369M | ✅ | 2024 |
| MENTALITY | 时域切段 | 时序+空间映射 | 无 | Mamba enc–dec | 信号+谱重构 MSE 取平均 | — | ✗ | 2024 |
| MMM | 微分熵特征 | 空间映射 | 空间（固定） | 时空 Transformer enc–dec | 掩码 DE 特征重构 MSE | — | ✅ | 2023 |
| Neuro-BERT | 时域切段 | 时序映射 | 时间（可学习） | 时序 Transformer enc + 轻量 decoder | 掩码傅里叶反演预测 MSE | ~0.8M | ✅ | 2025 |
| Neuro-GPT | 时域切段 | 空间+时序映射 | 无 | 时空 CNN encoder + 时序 Transformer decoder | 掩码自回归预测 MSE | — | ✅ | 2024 |
| NeuroLM | 时域切段 + VQ + EEG-文本对齐 | 空间+时序映射 | 空间+时间（全可学习） | 时空 Transformer decoder | 自回归预测 CE | 254–1696M | ✅ | 2025 |

**表内勘误**（站内核对）：FoME 年份印成 2021（应 2024）；表中 EEGPT 条目是 decoder 自回归、1–1090M 参数，实为站内 [BrainGPT](../fm/braingpt.md)（Yue et al.）而非站内 [EEGPT](../fm/eegpt.md)（Wang et al.）；BENDR 架构一栏「wav2dec」为笔误。

## 3 分类树（原 Figure 2 复现）

把上表 18 个模型按字段聚族：

**词元化五类 + 一个附加项**：

| 词元化 | 成员 |
|---|---|
| 时域切段（主流，12 篇） | BIOT、Brant 系、CBraMod、EEGPT（=站内 BrainGPT）、FoME、Gram、LaBraM、MENTALITY、Neuro-BERT、Neuro-GPT、NeuroLM |
| 频域切段 | EEGFormer（FFT 后按谱切段） |
| 时频切段 | BrainBERT、BrainWave（先做 2D 谱图再切） |
| 空时二维切段 | FEMBA（通道 × 时间二维块） |
| 微分熵特征 | MMM |
| 附加 VQ 量化 | EEGFormer、Gram、LaBraM、NeuroLM |

**输入嵌入四类**：时序映射（9 篇）、谱映射（6 篇）、空间映射（MENTALITY、MMM、Neuro-GPT、NeuroLM）、谱时/时空映射（BrainWave、FEMBA）；特例 BrainBERT 的 z-score 归一化与 EEGPT（=站内 BrainGPT）的无嵌入。

**位置编码三轴**：序列序（可学习：Brant 系、CBraMod、EEGFormer、FEMBA、FoME、LaBraM；固定正弦：BIOT、BrainBERT、Gram）；空间（可学习：BIOT、CBraMod、EEGPT=站内 BrainGPT、LaBraM、NeuroLM；固定：Gram、MMM）；时间（可学习：BENDR、Neuro-BERT、NeuroLM）。自回归模型（EEGPT=站内 BrainGPT、Neuro-GPT）时序由因果结构隐含，不另加 PE。

**骨干三族**：encoder（Transformer：BENDR、BIOT、BrainBERT、BrainWave、Brant 系、CBraMod、FoME、LaBraM）；encoder–decoder（Transformer：EEGFormer、Gram、MMM；Mamba：MENTALITY；混合：FEMBA、Neuro-BERT、Neuro-GPT）；decoder（EEGPT=站内 BrainGPT、NeuroLM）。

**目标与损失**：重构 14 篇（信号/特征直接重构 vs 离散 token 预测两型）、预测 3 篇（EEGPT=站内 BrainGPT、Neuro-GPT、NeuroLM）、混合 1 篇（Brant-2 同时做重构与预测）；损失对应 MSE（12 篇）、MAE/Smooth-L1（BrainBERT、FEMBA——对离群点更稳）、CE（Gram、LaBraM、NeuroLM——预测离散码字）、对比（BENDR、BIOT）。

patching 让长记录在算力上可行，代价是切段边界破坏细粒度时序模式——BENDR 因此不走切段，用卷积编码器直接对原始信号降采样；BrainBERT 则在切段前先做 superlet 变换取时频分辨率。VQ 的动机是连续分布难处理多模态，量化到码本「捕捉反复出现的模式」。

## 4 预训练语料（原 Table 2 精简）

| 模型 | 预训练语料 | 时长 | 模态 |
|---|---|---|---|
| BrainWave | CCEP ECoG、CAP、HMC、Siena、SRM、TUEG、Schizophrenia-81、Sleep-EDF、Stroke-50、PD-31、AD-184 等十余套 | 未报 | EEG + iEEG |
| Brant-2 | TUEG + 私有 iEEG | ~41,000 h | EEG + iEEG |
| CBraMod | TUEG | ~27,000 h | EEG |
| FoME | TUEG、SEED 系、CHB-MIT、Sleep-EDFx、MI 数据集、MAYO、FNUSA | ~26,000 h | EEG + iEEG |
| NeuroLM | LaBraM 语料族 + TUEG + 私有语料 | ~25,000 h | EEG + text |
| Gram | LaBraM 语料族 + TUAB/TUSZ + 自采（RUIJIN） | ~7,000 h | EEG |
| LaBraM | BCI Competition IV-1、Emobrain、Grasp/Lift、Inria、EEG Motor Movement、静息态、SEED 系、Siena、SPIS、TUAR/TUEP/TUSZ/TUSL、私有语料 | 2,535 h | EEG |
| BrainBERT / Brant | 私有 iEEG 语料（Brain TreeBank） | 4.5k channel-hours（表 1 口径） | iEEG |
| BIOT | SHHS、PREST、Cardiology | 未报 | EEG + ECG |
| EEGPT（=站内 BrainGPT） | FACED、SEED 系、THINGS-EEG、私有语料 | 未报 | EEG |
| MENTALITY / Neuro-GPT / FEMBA / EEGFormer / MMM | TUEG 或其子集 | 未报 | EEG |

数据侧结论：TUEG 与 SEED 系被最多模型用作预训练语料；时长口径混杂（小时 / channel-hours / 样本数），站内对照见 [Kuruppu 综述的口径表](kuruppu-critical-review.md)。作者点名 EEG 预训练语料相对 NLP/CV「小而少样」，并引 MMM 的一维位置编码 + 多级通道层次 + 多阶段预训练作为拓扑差异的应对。

## 5 迁移学习与不变表示

独立成章，可当下游适配的路线图。域偏移按四轴分：跨被试 / 跨会话 / 跨设备 / 跨任务。

**方法四类**：

| 类 | 机制 | 例子 |
|---|---|---|
| instance-based | 重加权或选择源域样本 | importance weighting、样本重加权、域适配分类器 |
| feature-based | 学共享特征空间降分布差 | 黎曼流形对齐、CSP 跨被试改造、预训练特征做域不变提取 |
| model-based | 微调预训练网络 | BrainBERT/EEGPT 式微调下游分类、CNN 小数据微调、GAN 增广适配 |
| classifier-based | 迁移决策边界 | DANN 梯度反转（被试/会话不变分类器）、集成加权投票 |

**不变表示三路**：对比学习（最大化被试间相似度的时空表示）、对抗推断（对抗域适配学被试不变特征）、因子化表示（低维 EEG 表示拆「共性内容 / 被试风格」，factorized hierarchical VAE 两个解耦隐空间）。

## 6 三个落地案例

- **SELSER**（抑郁生物标志物）：空间滤波 + 频带功率 + 线性回归在稀疏潜空间里全局最优求解，预测舍曲林疗效 HAMD 变化 r=0.6（p=5.19×10⁻¹¹）；同一模型放到安慰剂臂 r=−0.03，阴性对照符合预期。
- **Brant-X**（多模态对齐）：冻结 Brant-2（预训练 4 TB+ EEG）作 EEG 端，EXG 端新训编码器，patch 级 + 序列级两级对比对齐；任务跨睡眠分期（EEG+EOG）、情绪（EEG+ECG）、冻结步态（EEG+EMG）、眼动交流。
- **NeuroLM**（多任务指令微调）：VQ 词元器 + LLM 因果建模 + 多任务指令微调，预训练 25 000 h，单模型跨六任务推理（异常检测 / 情绪 / 睡眠分期 / 认知负荷 / 事件分类 / 慢波分类）。

## 7 规模、可解释性与开放科学

Scaling 证据：LaBraM 的模型/数据双缩放实验；非侵入语音解码单被试 175 h→48% vs 10 h→2.5% top-1，作者预期 FM 性能随 10 000 h 量级语料继续提升。可解释性一节超出注意力可视化范畴：归因分析（积分梯度、SHAP）、概念激活向量、因果表示学习的可辨识性定理（LLM 隐空间中概念线性编码的实证）、白盒 energy transformer。数据一节给了公开语料库清单（Harvard 28 万+ 记录、UCSD NEMAR 2.7 万被试、OpenNeuro、PhysioNet 等）并点名地理/性别/年龄偏置。讨论直言「Are large-scale foundation models all we need? The simple answer is no.」——灾难性遗忘、模型脆弱性（对抗噪声、解释本身也脆弱）、数据质量与开放科学三节均值得引用。

## 8 站内视角

- 词元化五分类与本站 [Tokenization 演进专题](../../topics/tokenization.md) 口径最接近：它按「切段几何」分类，站内按「词表来源与用途」分类；写词元化节时先引该文分类，再给站内对照。
- TL 四分类与本站 REVE 微调策略（缓存线性探针 → 小学习率微调）同属 model-based 一支，可直接引用其框架。
- 与同期 [Kuruppu 批判性综述](kuruppu-critical-review.md) 相比，这篇覆盖面更广、批判较少（「独立验证仍缺」一句带过）；两表的字段口径互补（本表含损失与开源，Yao 表含注意力机制与数据集）。

---

**相关阅读**

:material-call_split: [Tokenization 演进专题（与词元化五分类对照）](../../topics/tokenization.md) ｜ :material-link-variant: [LaBraM（Table 1 中 VQ 谱预测一支）](../fm/labram.md) ｜ :material-tag-multiple: [NeuroLM（EEG-文本对齐 + 指令微调案例）](../fm/neurolm.md) ｜ :material-magnify-remove-outline: [EEGPT（注意与表中条目同名不同人）](../fm/eegpt.md) ｜ :material-format-list-bulleted: [Yao 综述（技术设计表口径互补）](yao-eegfm-survey.md) ｜ :material-clipboard-check: [Kuruppu 批判性综述（同期更严的对照）](kuruppu-critical-review.md)
