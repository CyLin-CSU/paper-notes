---
title: 语音模型专题
tags: [语音解码, mel谱, wav2vec, EEG-to-Text, 综述]
---

# 语音模型专题：脑信号 → 语音与文本

按输入表示、训练目标和下游输出，对照 [Défossez](../papers/defossez-speech.md)、[SSM2Mel](../papers/ssm2mel.md) 与 [DELTA](../papers/delta.md)。

## 总览

| 论文 | 脑信号输入 | 目标表示 | 下游输出 |
|---|---|---|---|
| Défossez | 连续脑信号，含 EEG / MEG | 语音 embedding | 语音候选的相似度 |
| SSM2Mel | 连续 EEG | mel 时频图 | 连续 mel 时频图 |
| DELTA | 词级 EEG 特征 | 离散 EEG token 与文本 token | 文本 |

- **Défossez**：对齐脑信号与预训练语音模型的表示，在候选集中检索听到的语音。

- **SSM2Mel**：用状态空间模型与注意力，从 EEG 直接回归 mel 时频图。

- **DELTA**：先把词级 EEG 特征量化为离散 token，再用掩码语言模型生成文本。

## 一、输入如何编码

| 论文 | 信号编码 | 通道 / 被试处理 | 离散码表 |
|---|---|---|---|
| Défossez | 连续卷积提取信号 embedding | 空间注意力统一通道；被试专属线性层 | 无码表 |
| SSM2Mel | 局部特征提取 + 状态空间模型与注意力 | 被试 embedding 调制特征 | 无码表 |
| DELTA | 词级 EEG 特征经过卷积 encoder 与 RVQ | 固定通道与频段配置，组织成词级特征 | RVQ 码表 |

- **Défossez**：不按固定 patch 建词表，连续脑信号表示与语音 embedding 做时间对齐。

- **SSM2Mel**：在连续特征序列上建模，mel 时频图是输出目标。

- **DELTA**：每个阅读词语对应一组 EEG 特征，经过 RVQ 得到多层离散 token。输入已经按词语组织，区别于对任意连续 EEG 直接解码。

## 二、Tokenizer 与主模型如何训练

### Tokenizer

| 论文 | 码表 | 掩码部分 | 重建部分 |
|---|---|---|---|
| Défossez | 无码表 | — | — |
| SSM2Mel | 无码表 | — | — |
| DELTA | RVQ 码表 | 不掩码 | 词级 EEG 特征 |

DELTA 用特征重构与 VQ 损失训练 tokenizer，不重建原始波形或时频图。

### 主模型

| 论文 / 阶段 | 训练输入 | 预测 / 对齐目标 |
|---|---|---|
| Défossez | 脑信号与配对语音 | 语音 embedding |
| SSM2Mel | EEG 与配对语音 | mel 时频图 |
| DELTA：EEG 适配 | 被掩 EEG token | 离散 EEG token |
| DELTA：文本微调 | EEG token + 被掩文本 token | 文本 token |

- **Défossez**：冻结 wav2vec 2.0，训练脑端 encoder；对比损失让配对语音表示的相似度高于其他候选。

- **SSM2Mel**：端到端监督回归 mel 时频图，没有独立的自监督预训练阶段。

- **DELTA**：加载 LLaDA-8B，用 QLoRA 进行 EEG token 掩码预训练与文本微调。文本微调时只掩码文本，EEG token 作为条件保留。

## 三、下游如何使用

| 论文 | 推理过程 | 输出范围 |
|---|---|---|
| Défossez | 脑信号 embedding 与候选语音 embedding 比相似度 | 从给定候选集中选择 |
| SSM2Mel | EEG 输入监督回归模型 | 输出连续 mel 时频图 |
| DELTA | EEG token 作为条件，从全掩码文本开始迭代预测 | 生成文本 token |

- **Défossez**：检索结果依赖候选集的组成与大小，需要明确候选如何构造。

- **SSM2Mel**：输出的是语音表征；从 mel 时频图合成可听语音，还需要对应的声码器。

- **DELTA**：输入依赖词级 EEG 特征的构造；评测时需说明是否使用真实前文，以及训练和测试文本如何划分。

## 四、数据与训练范围

| 论文 | 数据来源 | 训练范围 |
|---|---|---|
| Défossez | 4 个脑信号–语音配对数据集，含 EEG 与 MEG | 多被试联合训练，被试层分别设置 |
| SSM2Mel | SparrKULee | 配对 EEG–语音监督训练 |
| DELTA | ZuCo 1.0 + 2.0 | 用训练集学习 RVQ 词表，并适配 LLaDA |

- **Défossez**：脑端 encoder 从零训练，复用的是预训练语音模型提供的目标表示。

- **SSM2Mel**：不加载外部预训练基座。

- **DELTA**：复用预训练语言模型，但 EEG 适配数据仍来自 ZuCo，不视作额外的大规模通用 EEG 预训练。

## 关联页面

[Défossez 笔记](../papers/defossez-speech.md) · [SSM2Mel 笔记](../papers/ssm2mel.md) · [DELTA 笔记](../papers/delta.md)

[Tokenization](tokenization.md) · [预训练](pretraining.md) · [通道适配与多任务](multi-task.md) · [预训练数据](data-landscape.md) · [基座与参数量](base-model.md)

原文：[Défossez](https://doi.org/10.1038/s42256-023-00714-5) · [SSM2Mel](https://arxiv.org/abs/2501.10402) · [DELTA](https://arxiv.org/abs/2511.21746)。
