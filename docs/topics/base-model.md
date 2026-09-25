---
title: 基座来源：从零训练还是站在巨人肩上
tags: [基座模型, 综述]
---

# 基座来源：从零训练还是站在巨人肩上

> 六篇基础模型的权重是"自己从零训练"还是"加载现成 Base Model"？结论：**五篇从零训练，唯一例外是 NeuroLM 站在 GPT-2 上**。

## 总览表

| 论文 | 预训练权重来源 | 说明 |
|---|---|---|
| [BIOT](../papers/2026-09/0918-biot.md) | **从零训练** | 3.2M 小模型，自己在 PREST+SHHS 上做无监督预训练，无任何外部权重 |
| [LaBraM](../papers/2026-09/0918-labram.md) | **从零训练** | 架构借鉴 ViT（QK LayerNorm 等 trick），但 VQ tokenizer 和 Transformer 全部在自家 2500h 语料上从零训练 |
| [EEGPT](../papers/2026-09/0918-eegpt.md) | **从零训练** | 采用 ViT 代码实现，但 encoder/predictor/reconstructor 权重全在 5 个数据集上从零预训练 |
| [BrainGPT](../papers/2026-09/0918-braingpt.md) | **从零训练** | 架构是标准 GPT 式（因果注意力+Swish 门控 FFN），但权重完全靠 EEG 自回归预训练学出，没有加载任何语言模型权重 |
| [NeuroLM](../papers/2026-09/0918-neurolm.md) | **有基座：GPT-2** | 唯一例外——LLM 部分直接加载预训练 GPT-2，再在 EEG token 上做多通道自回归预训练 + 指令微调；VQ encoder 半边仍从零训练 |
| [TFM-Tokenizer](../papers/2026-09/0918-tfm-tokenizer.md) | **从零训练** | tokenizer（1.2M）+ 下游 Transformer（0.7M）都从零训 |

## 为什么几乎都不用现成基座

1. **当时不存在可用的 EEG 基座**。这几篇本身就是"第一批"基础模型，没有前人 EEG 权重可站（LaBraM/BIOT 互为对照，但都各自从零训练以保证公平）。
2. **模态鸿沟**。NLP/视觉的预训练权重对连续时序信号的迁移价值很低——加载了反而要花算力"遗忘"文本先验。
3. **NeuroLM 是唯一例外恰因范式不同**。它要把 EEG token 塞进 LLM 做指令推理，GPT-2 的语言能力（理解问题、生成答案）正是需要保留的部分——所以保留基座 + 词表扩充 + 继续训练而非从零。其消融也证明每批混入纯文本数据对防止语言能力遗忘是必要的。

## "复用权重"发生在下游而不是预训练

虽然预训练都是自力更生，但每篇都**开源了自己的预训练 checkpoint**（LaBraM Base/Large/Huge、EEGPT、BIOT、NeuroLM、TFM 均在 GitHub 发布），下游任务是站在这些**自家预训练权重**上微调的。

论文互相比时也不加载对方从头训的中间权重，而是：**基线 = 对方的公开 checkpoint + 我们数据集上的微调**。这也解释了 BrainGPT 的一个著名发现——"预训练 specialist 有时不如 from scratch"：LaBraM 语料偏临床癫痫，对情绪/运动想象等非临床任务迁移反而打折（详见[预训练数据全景](data-landscape.md)）。

## 新论文入库提示

读新论文时记一笔：它的权重是 **from scratch / 加载公开 EEG 基座（哪家）/ 接 LLM（哪个）** 三者中的哪一种？这决定了它与库里已有论文的可比性，也直接影响[互怼链](../comparison.md#critique-chain)的画法。

## 关联页面

[预训练数据全景](data-landscape.md) · [多任务三条路线](multi-task.md) · [六篇方法对比](../comparison.md)
