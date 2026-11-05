---
title: 预训练范式对比
tags: [预训练, 综述]
---

# 预训练范式对比

## 一、Tokenizer 如何训练

### 词表

| 论文 | 码表 | 掩码部分 | 重建部分 | 损失 |
|---|---|---|---|---|
| BIOT | 无码表 | — | — | — |
| LaBraM | VQ 码表 | **不掩码** | **频谱幅值 + 相位** | 幅值 MSE + 相位 MSE + VQ 损失 |
| EEGPT | 无码表 | — | — | — |
| BrainGPT | 无码表 | — | — | — |
| NeuroLM | VQ 码表 | **不掩码** | **原始信号 patch + 频谱幅值** | 信号 MSE + 幅值 MSE + VQ 损失 + EEG–文本域对抗损失 |
| TFM | VQ 码表 | **时频图** | **时频图** | 时频图 MSE + VQ 损失 |
| CBraMod | 无码表 | — | — | — |
| LUNA | 无码表 | — | — | — |
| REVE | 无码表 | — | — | — |
| EEGMoE | 无码表 | — | — | — |
| NeuroRVQ | 多尺度 RVQ 码表 | **不掩码** | **频谱幅值 + 相位**，并约束还原信号 | 对数幅值 MSE + 相位余弦损失 + 信号 MSE + commitment loss |
| BrainRVQ | 时域 / 频域双 RVQ 码表 | **不掩码** | **原始信号 patch + 频谱幅值 + 相位** | 信号 MSE + 幅值 MSE + 相位 MSE + commitment loss |
| CodeBrain | 时域 / 频域双 VQ 码表 | **不掩码** | **原始信号 patch + 频谱幅值 + 相位** | 重构 MSE + 时域对比损失 + VQ 损失 |
| NeuroDETR | 时间多尺度 / 空间金字塔 VQ 码表 | **不做随机掩码** | **信号 embedding** | 特征 MSE + commitment loss，与事件检测损失联合训练 |
| DELTA | RVQ 码表 | **不掩码** | **词级 EEG 特征** | 特征 MSE + VQ 损失 |


**VQ 的稳定性技巧**：LaBraM / TFM 用 **EMA 更新 codebook**，稳定词表。

**NeuroDETR**：VQ 随监督检测一起训练，没有独立的通用 tokenizer 预训练阶段。

**对称掩码**（LaBraM 提出，TFM 沿用）：mask 与其补集各做一次——两个互补视角；

- **LaBraM**：用于主模型的离散 token 预测。

- **TFM**：用于 tokenizer 的时频图重建。


## 二、主模型预测目标

### ① 对比学习：BIOT

| 论文 | 扰动部分 | 预测部分 | 损失 |
|---|---|---|---|
| BIOT | **原始信号 patch**（丢弃部分通道和时间片段） | **信号 embedding** | 对比交叉熵 |

原始与扰动共享 encoder，扰动侧再接 predictor。

### ② 掩码建模

| 论文 | 掩码部分 | 重建 / 预测部分 |
|---|---|---|
| LaBraM | **信号 embedding** | **离散 token** |
| TFM | **离散 token** | **离散 token** |
| EEGPT | **原始信号 patch** | **信号 embedding + 原始信号 patch** |
| CBraMod | **原始信号 patch** | **原始信号 patch** |
| LUNA | **信号 embedding** | **原始信号 patch** |
| EEGMoE | **信号 embedding** | **信号 embedding** |
| NeuroRVQ | **信号 embedding** | **离散 token** |
| BrainRVQ | **信号 embedding** | **离散 token** |
| CodeBrain | **原始信号 patch** | **离散 token** |
| REVE | **原始信号 patch**（时空块掩码 55%，空间 3cm / 时间 3s 连续块 + 10% 整通道 dropout） | **原始信号 patch** + 全局 token 二次重构（attention pooling 跨全部 MHA 层，信息瓶颈） |

**方法创新**：

- **LaBraM**：① **频谱监督的离散词表**，用幅值 + 相位训练 tokenizer，再给主模型提供预测标签；② **对称掩码**，mask 与其补集各训练一次，同一样本获得两个互补视角。

- **TFM**：① **单通道时频 motif 词表**，时域与频域双路径捕捉局部模式，不绑定固定通道布局；

- **EEGPT**：① **表示对齐 + 信号重构双目标**，路径1映射信号到潜空间进行掩码重构，路径2掩码重构原始信号，两路径最后损失相加。
- **CBraMod**：① **十字交叉注意力**，分别建模同一时刻的跨通道关系、同一通道的跨时间关系；② **非对称卷积位置编码（ACPE）**，从时空邻域动态生成位置信息。
- **LUNA**：① **可学习 query查询向量统一通道**，把不同电极布局映射到固定大小的隐空间；② **时间注意力只在隐空间计算**，减少对原始通道数的计算依赖。
- **EEGMoE**：① **特殊+共享的双专家组**，分别学习域特性与域共性；② **按 token 路由**，Top-K 选择特定专家，共享专家始终参与。


- **NeuroRVQ**：① **多尺度 + 多层残差量化**，一个 patch 用多组离散 token 表示；② **相位圆周约束**，用相位的正弦 / 余弦表示计算损失，避免直接回归角度的跳变。
- **BrainRVQ**：① **时域 / 频域双 RVQ**，分别保留波形与频谱信息；② **粗到细预测码字**，后一级依赖前一级，并优先掩码信息丰富的位置。
- **CodeBrain**：① **时域 / 频域双码表**，时域额外用对比学习稳定表示；② **全局卷积 SSM + 局部注意力**，分别处理长程关系与局部模式。

### ③ 自回归：BrainGPT / NeuroLM / BrainRVQ

| 论文 | 注意力可见范围 | 预测部分 | 损失 |
|---|---|---|---|
| BrainGPT | **同通道的当前及过去** | 同通道下一时刻的**原始信号 patch** | MSE |
| NeuroLM | **所有通道的当前及过去** | 同通道下一时刻的**离散 token** | 交叉熵 |
| BrainRVQ | **可见 patch + 同一位置较粗层的码字** | 被掩位置下一层的**离散 token** | 分层交叉熵 |

BrainGPT / NeuroLM 的掩码限制**注意力可见范围**，不随机挖掉输入。

- **BrainGPT**：在序列开头加入电极条件 token，预测下一时刻的原始信号 patch。

- **NeuroLM**：冻结 VQ encoder，加载 GPT-2 并扩充 EEG 词表，预测下一时刻的离散 token。

**NeuroLM 防遗忘**：预训练与指令微调都混入少量纯文本。

**BrainRVQ 的自回归在码字层级上**：同一 patch 从粗到细预测 RVQ 码字，不是沿时间预测下一个 patch。


### ④ 相关方法：NeuroDETR

| 论文 | 输入 | 预测部分 | 训练方式 |
|---|---|---|---|
| NeuroDETR | **连续原始信号** | **事件类别 + 起止时间** | 监督事件检测，与 VQ 特征重建联合训练 |

**方法创新**：① **FOCAL 事件感知注意力**，把计算集中到可能出现事件的片段；② **时间多尺度 VQ + 空间金字塔 VQ**，形成事件记忆，再由 query 联合预测类别与边界。它不属于上面的随机掩码预训练。

### ⑤ 配对解码与前端训练

| 论文 | 训练输入 | 预测 / 对齐目标 |
|---|---|---|
| [DELTA](../papers/delta.md) | 被掩 EEG token；EEG token + 被掩文本 token | 第一阶段预测 EEG token；第二阶段预测文本 token |
| [GUIDED](../papers/guided.md) | EEG 与配对图像 | CLIP 图像 embedding；生成阶段学习图像先验 |
| [Défossez](../papers/defossez-speech.md) | 脑信号与配对语音 | 语音 embedding |
| [SSM2Mel](../papers/ssm2mel.md) | EEG 与配对语音 | mel 时频图 |
| [LTFT](../papers/learnable-tf.md) | EEG 与任务标签 | 分类标签 |

- **DELTA**：先训练 RVQ tokenizer，再用掩码 EEG token 适配 LLaDA；文本微调时保留 EEG 条件，只掩码文本。

- **GUIDED**：脑端对齐预训练 CLIP 的图像 embedding；重建图像时，再训练 EEG 条件的扩散先验。

- **Défossez**：冻结语音模型，用配对数据对比对齐脑信号与语音表示。

- **SSM2Mel**：直接监督回归 mel 时频图，未设置独立的自监督预训练阶段。

- **LTFT**：分类损失同时更新时频窗口与下游网络，未设置独立的 tokenizer 训练阶段。

这几种方法的输出目标不同，配对解码与通用 EEG 表示预训练分开列。

### 关联论文

[BIOT](../papers/biot.md) · [LaBraM](../papers/labram.md) · [EEGPT](../papers/eegpt.md) · [BrainGPT](../papers/braingpt.md) · [NeuroLM](../papers/neurolm.md) · [TFM-Tokenizer](../papers/tfm-tokenizer.md) · [CBraMod](../papers/cbramod.md) · [LUNA](../papers/luna.md) · [EEGMoE](../papers/eegmoe.md) · [JET](../papers/jet.md) · [EEGDM](../papers/eegdm.md) · [Not-All-EEG](../papers/not-all-eeg.md) · [RF-GPT](../papers/rf-gpt.md)

新增论文原文：[NeuroRVQ](https://arxiv.org/abs/2510.13068) · [BrainRVQ](https://arxiv.org/abs/2602.16951) · [CodeBrain](https://arxiv.org/abs/2506.09110) · [NeuroDETR](https://arxiv.org/abs/2610.20349)。
