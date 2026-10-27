---
title: 基座来源：从零训练还是站在巨人肩上
tags: [基座模型, 综述]
---

# 基座来源：从零训练还是站在巨人肩上

> 十二篇的权重是「自己从零训练」还是「加载现成 Base Model」？结论：**十篇从零训练，两例借底座**——NeuroLM 站在 GPT-2 上（EEG 编码器仍自训），RF-GPT 站在 Qwen2.5-VL 上（连信号编码器都不训，最彻底）。本页是[十二篇方法对比](../comparison.md)的「基座维度」深读页。

## 总览表

| 论文 | 预训练权重来源 | 说明 |
|---|---|---|
| [BIOT](../papers/2026-09/0918-biot.md) | **从零训练** | 3.2M 小模型，自己在 PREST+SHHS 上做无监督预训练，无任何外部权重 |
| [LaBraM](../papers/2026-09/0918-labram.md) | **从零训练** | 架构借鉴 ViT（QK LayerNorm 等 trick），但 VQ tokenizer 和 Transformer 全部在自家 2500h 语料上从零训练 |
| [EEGPT](../papers/2026-09/0918-eegpt.md) | **从零训练** | 采用 ViT 代码实现，但 encoder/predictor/reconstructor 权重全在 5 个数据集上从零预训练 |
| [BrainGPT](../papers/2026-09/0918-braingpt.md) | **从零训练** | 架构是标准 GPT 式（因果注意力+Swish 门控 FFN），但权重完全靠 EEG 自回归预训练学出，没有加载任何语言模型权重 |
| [NeuroLM](../papers/2026-09/0918-neurolm.md) | **有基座：GPT-2** | LLM 部分直接加载预训练 GPT-2，再在 EEG token 上做多通道自回归预训练 + 指令微调；VQ encoder 半边仍从零训练 |
| [TFM-Tokenizer](../papers/2026-09/0918-tfm-tokenizer.md) | **从零训练** | tokenizer（1.2M）+ 下游 Transformer（0.7M）都从零训 |
| [CBraMod](../papers/2026-09/0928-cbramod.md) | **从零训练** | 4.0M 十字交叉 Transformer 在 TUEG 清洗版上 MAE 式预训练；**已进 Braindecode，自己成了可被下游复用的 EEG 基座** |
| [LUNA](../papers/2026-09/0924-luna.md) | **从零训练** | 7M–311.4M 全系自训（TUEG+Siena 21,900h）；Base 版 14MB 面向可穿戴部署 |
| [EEGMoE](../papers/2026-09/0924-eegmoe.md) | **从零训练** | 1.68M SSMoE 编码器，~142h 认知域语料 |
| [JET](../papers/2026-09/0923-jet.md) | **从零训练** | 129.9M 生成 Transformer 从零训练（生成路线没有可借的 EEG 底座） |
| [EEGDM](../papers/2026-10/1017-eegdm.md) | **从零训练** | EEG-ViT encoder + DiT 去噪器完全从零联合训练（架构件 DiT/adaLN-Zero 是设计借鉴，非权重复用） |
| [RF-GPT](../papers/2026-09/0921-rf-gpt.md) | **有基座：Qwen2.5-VL** | **最彻底的借底座**：IQ→STFT 谱图直接复用预训练 VLM 的视觉编码器 + LLM 解码器，不训练任何信号编码器，只在合成指令对上 SFT（8×H200） |

## 为什么 EEG 侧几乎都不用现成基座

1. **起步期不存在可用的 EEG 基座**。核心六篇本身就是「第一批」基础模型，没有前人 EEG 权重可站（LaBraM/BIOT 互为对照，但都各自从零训练以保证公平）。2025 年后情况开始变化：CBraMod 已进 Braindecode、LUNA 开源全系规格——**下一代论文「加载公开 EEG 基座 + 微调」的路线已经打开**（EEG-FM-Compass 的统一复测实际上就是在做这件事）；
2. **模态鸿沟**。NLP/视觉的预训练权重对连续时序信号的迁移价值很低——加载了反而要花算力「遗忘」文本先验；
3. **两个例外各有各的道理**：
    - **NeuroLM 借 GPT-2**：它要把 EEG token 塞进 LLM 做指令推理，GPT-2 的语言能力（理解问题、生成答案）正是需要保留的部分——所以保留基座 + 词表扩充 + 继续训练而非从零。消融证明每批混入纯文本数据防遗忘是必要的；
    - **RF-GPT 借 Qwen2.5-VL**：成立的前提有两个——STFT 谱图「长得像图」，图像预训练的视觉编码器对其有通用语义先验（分辨率消融 224→512 单调提升佐证了视觉路径确实在利用时频细节）；合成数据「配置即标签」，零噪声监督让 SFT 一步到位。**这两个前提在 EEG 域都打了折扣**：没有标准波形生成器级别的仿真器；且通用 VLM「随机猜」的阴性对照（GPT-5 读 RF 谱图近随机）说明模态接地没有捷径——谱图先验≠免费读懂。

## "复用权重"发生在下游而不是预训练

虽然预训练都是自力更生，但各家都**开源了自己的预训练 checkpoint**（BIOT、LaBraM、EEGPT、NeuroLM、TFM、CBraMod、LUNA、EEGDM 均在 GitHub 发布），下游任务是站在这些**自家预训练权重**上微调的。

论文互相比时也不加载对方从头训的中间权重，而是：**基线 = 对方的公开 checkpoint + 我们数据集上的微调**。这也解释了 BrainGPT 的一个著名发现——「预训练 specialist 有时不如 from scratch」：LaBraM 语料偏临床癫痫，对情绪/运动想象等非临床任务迁移反而打折（详见[预训练数据全景](data-landscape.md)）。

一个对照细节：**LaBraM 的 Large/Huge 权重未开源**——后续论文（含 CBraMod 作者）只复现过 LaBraM-Base，各家表格里「打过 LaBraM-Huge」的数字多引自 LaBraM 原文，严格说不是同口径复测。

## 新论文入库提示

读新论文时记一笔：它的权重是 **from scratch / 加载公开 EEG 基座（哪家）/ 接 LLM（哪个）** 三者中的哪一种？这决定了它与库里已有论文的可比性，也直接影响[互怼链](../comparison.md#critique-chain)的画法。2026 年起第一类正在变多（借现成 EEG FM 或 VLM），记录时注明加载的具体 checkpoint 版本。

## 关联页面

[预训练数据全景](data-landscape.md) · [多任务与下游适配](multi-task.md) · [十二篇方法对比](../comparison.md)
