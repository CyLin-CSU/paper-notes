---
title: 通道适配与多任务学习
tags: [通道适配, 多任务, 迁移学习, 综述]
---

# 通道适配与多任务学习

先看两件事：**不同通道怎么输入同一个模型，不同任务怎么使用同一个模型**。通用表示学习、配对解码与基准评测分别说明。

## 一、通道如何适配 {: #channel-adaptation }

| 论文 | 通道表示 | 跨通道整合 |
|---|---|---|
| BIOT | **通道 embedding** | 跨通道注意力 |
| LaBraM | **通道 embedding** | 跨通道注意力 |
| EEGPT | **通道 embedding** | 注意力 + summary token 汇聚 |
| BrainGPT | **通道 embedding** | 单通道 encoder 提取表示，下游电极图整合 |
| NeuroLM | **通道 embedding** | 多通道自回归注意力 |
| TFM | **单通道 tokenizer，下游加通道 embedding** | 主模型跨通道注意力 |
| CBraMod | **动态位置编码（ACPE）** | 十字交叉注意力 |
| LUNA | **电极坐标编码** | 可学习 query 汇聚到固定隐空间 |
| EEGMoE | **统一脑地图** | 空间/频率编码器汇聚 |
| NeuroRVQ | **通道 embedding** | 跨通道注意力 |
| BrainRVQ | **通道 embedding** | 跨通道注意力 |
| CodeBrain | **动态位置编码（ACPE）** | 通道邻域编码 + EEGSSM 整合 |
| NeuroDETR | **电极坐标 + 脑区分组** | 虚拟通道混合 + 空间金字塔 VQ |

BIOT、LaBraM、EEGPT、BrainGPT、NeuroLM 的通道表覆盖范围与使用阶段不同，这里统一写成 **通道 embedding**。

- **LUNA**：根据电极坐标生成编码。

- **CBraMod**：根据输入邻域动态生成位置编码。

- **EEGMoE**：先在输入端统一电极网格。

### 单通道建模后，空间关系在哪里补

| 论文 | 单通道阶段 | 跨通道阶段 |
|---|---|---|
| BrainGPT | **单通道 encoder 预训练**，学习时间关系 | **下游电极图**，整合各通道表示 |
| TFM | **单通道 tokenizer 训练**，学习时频 motif | **主模型预训练与下游分类**，整合各通道 token |

- **TFM**：主模型预训练时已经学习跨通道关系。

- **BrainGPT**：下游阶段才通过电极图整合通道。

### 通道兼容的边界

- **通道 embedding**：依赖通道标识与已有向量表；缺通道、换通道数，与增加训练时未见的电极不是同一件事。
- **单通道 tokenizer / encoder**：降低输入端对固定布局的依赖；后面的通道 embedding、电极图或分类头仍需要适配。
- **动态位置编码 / 电极坐标编码 / 统一脑地图**：提供不同的空间表示方式，不等于已经解决所有跨设备分布差异。

## 二、下游如何适配不同任务 {: #task-adaptation }

| 论文 | 训练方式 | 训练的模块 | 任务之间怎么共享 |
|---|---|---|---|
| BIOT | **逐任务微调** | encoder + 分类头 | 共享预训练初始化，微调后各任务一份权重 |
| LaBraM | **逐任务微调** | encoder + 分类头 | 共享预训练初始化，微调后各任务一份权重 |
| EEGPT | **逐任务训练，冻结 encoder** | 通道适配模块 + 分类头 | 共享冻结 encoder，适配模块与分类头按任务训练 |
| BrainGPT | **多任务联合训练** | 电极图 + 任务分类头，冻结 encoder | 共享 encoder 与电极图，各任务保留分类头 |
| NeuroLM | **多任务指令微调** | LLM，冻结 tokenizer | 共享 LLM，用文本指令区分任务 |
| TFM | **逐任务微调** | encoder + 分类头，冻结 tokenizer | 共享 tokenizer 与预训练初始化，微调后各任务一份权重 |
| CBraMod | **逐任务微调** | encoder + 分类头 | 共享预训练初始化，微调后各任务一份权重 |
| LUNA | **逐任务微调** | encoder + 分类头 | 共享预训练初始化，微调后各任务一份权重 |
| EEGMoE | **逐任务微调** | encoder + 分类头 | 共享预训练初始化，微调后各任务一份权重 |
| NeuroRVQ | **逐任务微调** | encoder + 分类头 | 共享预训练初始化，微调后各任务一份权重 |
| BrainRVQ | **逐任务微调** | encoder + 分类头 | 共享预训练初始化，微调后各任务一份权重 |
| CodeBrain | **逐任务微调** | encoder + 分类头 | 共享预训练初始化，微调后各任务一份权重 |
| NeuroDETR | **逐数据集监督训练** | encoder + VQ + 事件检测头 | 不将多数据集评测等同于多任务联合训练 |

**多数据集预训练不等于下游多任务联合训练**：共同预训练后，各任务分别微调，最终仍是多份模型。EEGMoE 在预训练中用专家学习域共性与域特性，但下游仍逐任务微调。

**冻结与微调分开比较**：EEGPT 主要采用冻结 encoder 的探针协议；其他几种模型主要报告微调结果。不能直接把两种设定的成绩当成相同训练条件，也不能据此断言所有模型都必须微调。

## 三、各自最有特色的设计

- **BIOT**：① **逐通道切段后统一展平**，不同通道数与信号长度可以转成 token 序列；② **缺失片段直接丢弃对应 token**，不要求所有通道始终完整。

- **LaBraM**：① **按电极标识索引通道 embedding**，不同数据集映射到同一套空间表示；② **通道 patch 统一输入**，预训练 encoder 再逐任务微调。
- **EEGPT**：① **summary token 汇聚通道信息**，得到固定大小的时间段表示；② **冻结 encoder + 可训练通道适配模块**，把输入适配与特征提取分开。
- **BrainGPT**：① **单通道学时间，下游电极图学空间**；② **任务共享电极图**，同一电极的节点参数接受多个任务的梯度，任务区别由各自分类头保留。
- **NeuroLM**：① **EEG token + 文本指令**，把不同分类任务统一成回答问题；② **只对答案计算损失**，并混入纯文本防止语言能力遗忘。
- **TFM**：① **单通道 tokenizer 不绑定固定通道布局**，主模型再整合空间关系；② **tokenizer 可插拔**，可以接不同骨干，迁移词表与迁移主模型分开。
- **CBraMod**：① **十字交叉注意力**，分别建模跨通道与跨时间关系；② **ACPE 动态位置编码**，从输入的时空邻域生成位置信息。
- **LUNA**：① **电极坐标编码 + 可学习 query**，把不同通道集合映射到固定隐空间；② **时间注意力在隐空间计算**，降低计算量对原始通道数的依赖。
- **EEGMoE**：① **统一脑地图**处理输入布局；② **特定 + 共享双专家组**处理域差异，几何适配与域表征分工。

- **NeuroRVQ**：① **按模态调整 patch 与量化配置**，EEG、ECG、EMG 分别训练；② 下游使用 **encoder + 分类头微调**，不把多模态分别训练等同于共享一套模型。
- **BrainRVQ**：① **双域分层预训练**，下游仍迁移 encoder；② **逐任务微调**，并非一个模型同时输出多种任务答案。
- **CodeBrain**：① **ACPE 动态位置编码**处理通道邻域；② **全局卷积 SSM + 局部注意力**整合信号，分类时使用预训练 encoder。
- **NeuroDETR**：① **电极坐标混合 + 脑区分组**保留空间信息；② **query 事件检测头**同时预测类别与起止时间，区别于整段 EEG 的单标签分类。

**两个多任务机制的区别**：

- **BrainGPT**：共享电极图与骨干，各任务使用独立分类头。

- **NeuroLM**：共享 LLM，通过文本指令选择任务。

通道布局兼容与未见任务泛化，需要分别验证。

## 四、配对解码如何适配

| 论文 | 通道 / 被试处理 | 下游输出 |
|---|---|---|
| [Défossez](../papers/defossez-speech.md) | 空间注意力统一通道，每位被试设置独立线性层 | 语音候选的相似度 |
| [SSM2Mel](../papers/ssm2mel.md) | 被试 embedding 调制信号特征 | mel 时频图 |
| [DELTA](../papers/delta.md) | 词级 EEG 特征经 RVQ 编码，采用固定的通道与频段配置 | 文本 token |
| [GUIDED](../papers/guided.md) | 通道注意力 + 时空卷积提取脑信号表示 | 图像候选的相似度，或图像重建条件 |

- **DELTA**：用 QLoRA 适配 LLaDA，EEG token 作为文本生成条件；原文未验证跨任务共享同一套模型。

- **GUIDED**：同一个脑信号表示用于分类、检索与图像重建，但各任务使用的损失与解码模块不同。

## 五、跨被试、跨时间与通道评测

- **[CrossPT-EEG](../papers/crosspt-eeg.md)**：把被试内、跨被试、跨时间的视觉解码分开评测，检查模型是否依赖特定被试或记录时间。

- **[EEGArena](../papers/eegarena.md)**：统一数据划分、训练与评测接口，同时保留各模型的输入处理；分开比较预训练收益、数据规模和通道兼容性。

多任务共享、跨被试迁移、跨时间迁移是不同问题，需要分别注明训练与测试的数据关系。

### 关联论文

[BIOT](../papers/biot.md) · [LaBraM](../papers/labram.md) · [EEGPT](../papers/eegpt.md) · [BrainGPT](../papers/braingpt.md) · [NeuroLM](../papers/neurolm.md) · [TFM](../papers/tfm-tokenizer.md) · [CBraMod](../papers/cbramod.md) · [LUNA](../papers/luna.md) · [EEGMoE](../papers/eegmoe.md)

[预训练范式对比](pretraining.md) · [EEG Tokenization 演进](tokenization.md) · [十三篇方法对比](../comparison.md)

新增论文原文：[NeuroRVQ](https://arxiv.org/abs/2510.13068) · [BrainRVQ](https://arxiv.org/abs/2602.16951) · [CodeBrain](https://arxiv.org/abs/2506.09110) · [NeuroDETR](https://arxiv.org/abs/2610.20349)。
