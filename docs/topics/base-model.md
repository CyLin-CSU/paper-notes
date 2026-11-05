---
title: 基座来源与模型参数量
tags: [基座模型, 模型规模, 综述]
---

# 基座来源与模型参数量

**架构借鉴与预训练权重复用分开看**。主模型与 tokenizer 分别统计，配对解码使用的外部基座另列。

## 总览表

| 论文 | 预训练权重来源 | 主模型参数量 | Tokenizer 参数量 | 说明 |
|---|---|---|---|---|
| [BIOT](../papers/biot.md) | **从零训练** | 3.2M | — | EEG encoder 从零预训练 |
| [LaBraM](../papers/labram.md) | **从零训练** | 5.8M / 46M / 369M | 约 8.6M | tokenizer 与主模型分别训练；分类时不使用 tokenizer |
| [EEGPT](../papers/eegpt.md) | **从零训练** | 约 25M（公开 Large encoder） | — | 只计 encoder，不合计 predictor、reconstructor 与 momentum encoder |
| [BrainGPT](../papers/braingpt.md) | **从零训练** | 1.46M / 11.29M / 183.8M / 1.09B | — | GPT 式架构，不加载语言模型权重 |
| [NeuroLM](../papers/neurolm.md) | **GPT-2 基座** | 扩词后未单列；基座约 124M / 355M / 1.56B | VQ encoder 未单列 | GPT-2 继续预训练与指令微调，VQ encoder 从零训练 |
| [TFM](../papers/tfm-tokenizer.md) | **从零训练** | 约 0.7M | 约 1.2M | 分类时保留 tokenizer，两者合计约 1.9M |
| [CBraMod](../papers/cbramod.md) | **从零训练** | 4.0M | — | 十字交叉 Transformer 从零预训练 |
| [LUNA](../papers/luna.md) | **从零训练** | 7M / 43M / 311.4M | — | Base / Large / Huge 三种规模 |
| [REVE](../papers/reve.md) | **从零训练** | 12M / 69M / 408M | — | MAE 从零预训练；encoder 权重开源，decoder 因隐私不发布 |
| [EEGMoE](../papers/eegmoe.md) | **从零训练** | 1.68M（激活 0.89M） | — | 总参数量与每次激活参数量分开列 |
| [NeuroRVQ](https://arxiv.org/abs/2510.13068) | **从零训练** | 5.9M（EEG backbone） | 随模态与 RVQ 配置变化，采用值未单列 | 只列 EEG 主模型，不合计分类头与 tokenizer |
| [BrainRVQ](https://arxiv.org/abs/2602.16951) | **从零训练** | 5.82M（12 层 encoder） | 未单列 | 双域 RVQ + 分层码字预测，下游使用 encoder |
| [CodeBrain](https://arxiv.org/abs/2506.09110) | **从零训练** | 15.17M（EEGSSM） | 未单列 | tokenizer 提供预训练目标，分类时微调主模型 |
| [NeuroDETR](https://arxiv.org/abs/2610.20349) | **监督训练，未报告外部基座** | 未单列 | 未单列，与检测模型联合训练 | 事件检测模型，不填作通用预训练 backbone |

**参数口径**：M = 百万，B = 十亿；主模型与 tokenizer 分开统计。“—”表示无独立离散 tokenizer。

- **EEGPT**：按官方 Large encoder 结构估算。

- **NeuroLM**：基座数字不包含扩词与新增模块，含 VQ encoder 的总量不作为 LLM 参数量。

## 配对解码方法的权重来源

| 论文 | 训练的脑信号模型 | 复用的预训练模型 | 参数量口径 |
|---|---|---|---|
| [DELTA](../papers/delta.md) | RVQ tokenizer 从零训练 | LLaDA-8B，用 QLoRA 适配 | 主模型为 8B 基座；tokenizer 未单列 |
| [GUIDED](../papers/guided.md) | ATM encoder 与 EEG 条件扩散先验 | CLIP、SDXL 等视觉模型 | ATM encoder 约 3.18M；不把冻结视觉模型计入脑端参数量 |
| [Défossez](../papers/defossez-speech.md) | 卷积脑信号 encoder 从零训练 | 冻结的 wav2vec 2.0 | 脑端参数量未在本专题单列 |
| [SSM2Mel](../papers/ssm2mel.md) | EEG 到 mel 的监督模型从零训练 | 未加载外部预训练基座 | 主模型参数量未单列 |

- **LTFT**：学习的是时频窗口与任务网络，不依赖外部预训练权重。

- **CrossPT-EEG / EEGArena**：属于数据与评测基准，不作为一款主模型统计参数量。

## 关联页面

[预训练数据全景](data-landscape.md) · [通道适配与多任务学习](multi-task.md) · [十四篇方法对比](../comparison.md)

新增论文原文：[NeuroRVQ](https://arxiv.org/abs/2510.13068) · [BrainRVQ](https://arxiv.org/abs/2602.16951) · [CodeBrain](https://arxiv.org/abs/2506.09110) · [NeuroDETR](https://arxiv.org/abs/2610.20349)。
