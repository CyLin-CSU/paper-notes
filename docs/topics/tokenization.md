---
title: EEG Tokenization 演进
tags: [tokenization, 综述]
---

# EEG Tokenization 演进

## 论文代码开源情况

| 论文 | 代码 | 备注 |
|---|---|---|
| [BIOT](../papers/biot.md) | [ycq091044/BIOT](https://github.com/ycq091044/BIOT) | 完整开源 |
| [LaBraM](../papers/labram.md) | [935963004/LaBraM](https://github.com/935963004/LaBraM) | 仅 Base 权重；Large / Huge 未放 |
| [EEGPT](../papers/eegpt.md) | [BINE022/EEGPT](https://github.com/BINE022/EEGPT) | 开源 |
| [NeuroLM](../papers/neurolm.md) | [935963004/NeuroLM](https://github.com/935963004/NeuroLM) | 开源 |
| [TFM-Tokenizer](../papers/tfm-tokenizer.md) | [Jathurshan0330/TFM-Tokenizer](https://github.com/Jathurshan0330/TFM-Tokenizer) | 含预训练权重与全部预处理脚本 |
| [CBraMod](../papers/cbramod.md) | [wjq-learning/CBraMod](https://github.com/wjq-learning/CBraMod) | 已进 Braindecode |
| [LUNA](../papers/luna.md) | [pulp-bio/biofoundation](https://github.com/pulp-bio/biofoundation) | Base / Large / Huge 全系 |
| [EEGDM](../papers/eegdm.md) | [wangsc18/EEGDM](https://github.com/wangsc18/EEGDM) | 含预处理脚本与训练配置 |
| [JET](../papers/jet.md) | [项目页](https://y-research-sbu.github.io/JET/) | 代码 / 权重以项目页为准 |
| [EEGMoE](../papers/eegmoe.md) | — | 论文声明将放出，精读时未见仓库 |
| [RF-GPT](../papers/rf-gpt.md) | — | 论文未附仓库（底座 Qwen2.5-VL 等组件公开可得） |
| [NeuroRVQ](../papers/neurorvq.md) | [项目页](https://neurorvq.github.io) · [Hugging Face](https://huggingface.co/ntinosbarmpas/NeuroRVQ) | 官方实现挂 HF（另有第三方 [Rust 推理](https://github.com/eugenehp/neurorvq-rs)） |
| [BrainRVQ](../papers/brainrvq.md) | [keqicmz/BrainRVQ](https://github.com/keqicmz/BrainRVQ) | 代码可访问，权重承诺论文接收后放出 |
| [CodeBrain](../papers/codebrain.md) | [jingyingma01/CodeBrain](https://github.com/jingyingma01/CodeBrain) | ICLR 2026 官方开源 |
| [NeuroDETR](../papers/neurodetr.md) | — | 暂未检索到官方仓库 |
| [DELTA](../papers/delta.md) | — | 论文未附仓库（NeurIPS 2025 Workshop） |

| 时间 | 论文 | Token 形态 | 词表 | Token 的用途 |
|---|---|---|---|---|
| 2023 | [BIOT](../papers/biot.md) | 信号 embedding（STFT 频谱帧投影） | 无码表 | 模型输入 |
| 2024 | [LaBraM](../papers/labram.md) | 离散 token（VQ） | 有 | **仅作预训练目标**，推理时丢弃 |
| 2024 | [EEGPT](../papers/eegpt.md) | 信号 embedding | 无码表 | 模型输入 |
| 2024 | [BrainGPT](../papers/braingpt.md) | 信号 embedding | 无码表 | 模型输入 |
| 2025 | [NeuroLM](../papers/neurolm.md) | 离散 token（VQ） | 有（并入 GPT-2 词表） | LLM 的输入 |
| 2026 | [TFM-Tokenizer](../papers/tfm-tokenizer.md) | 离散 token（时频 motif） | 有 | 模型输入 + 可插拔复用 |
| 2025 | [CBraMod](../papers/cbramod.md) | 信号 embedding | 无码表 | 模型输入 |
| 2025 | [LUNA](../papers/luna.md) | 信号 embedding | 无码表 | 模型输入 |
| 2026 | [EEGMoE](../papers/eegmoe.md) | 信号 embedding | 无码表 | 模型输入 |
| 2025 | [NeuroRVQ](../papers/neurorvq.md) | 离散 token（多尺度 RVQ） | 多尺度、多层码表 | 预训练目标 |
| 2026 | [BrainRVQ](../papers/brainrvq.md) | 离散 token（双域 RVQ） | 双域、多层码表 | 分层预训练目标 |
| 2026 | [CodeBrain](../papers/codebrain.md) | 离散 token（双域 VQ） | 双域码表 | 预训练目标 |
| 2026 | [NeuroDETR](../papers/neurodetr.md) | 时间多尺度 / 空间金字塔离散 token | 时间 / 空间码表 | 事件检测模型的输入记忆 |
| 2025 | [DELTA](../papers/delta.md) | 离散 token（词级 RVQ） | 自训多层码表 | 掩码语言扩散的输入 |

## 预处理与归一化异构信号

**重采样**：

- **BIOT / CBraMod / EEGDM / JET**：统一到 200Hz。

- **EEGPT / LUNA**：统一到 256Hz。

**滤波与归一化**：

- **BIOT**：逐通道除以绝对幅值的 95 分位数。

- **CBraMod**：0.3–75Hz 带通、60Hz 陷波，以 100µV 为单位归一。

- **LUNA**：0.1–75Hz 带通、50/60Hz 陷波，逐通道 z-score。

- **JET**：信号幅值整体乘 0.01。

## 片段细粒度

**patch 长度与重叠**：

- **LUNA**：40 点，256Hz 下约 0.16s。

- **EEGPT**：64 点，256Hz 下为 250ms。

- **BIOT**：1s STFT 窗，步长 0.5s；每个时间帧的频谱投影为 token。

- **TFM**：1s 窗、0.5s 步长，每个窗内继续建模时频结构。

- **LaBraM / CBraMod / EEGDM / JET**：主要使用 1s patch。

- **BrainRVQ / CodeBrain**：使用 1s 非重叠 patch。

**其他输入组织方式**：

- **EEGMoE**：先分频带，再按电极位置摆成脑地图，用空间与频率编码器提取表示。

- **RF-GPT**：把 STFT 时频图作为图片输入视觉语言模型。

- **DELTA**：按词语组织 EEG 特征，切分单位由配对阅读任务确定。

## 对token切分的总结

- **NeuroRVQ**：在 patch 内用多尺度卷积提取表示，每个尺度分别做 RVQ。

- **BrainRVQ**：同一 patch 分别量化为时域与频域两组残差码字。

- **CodeBrain**：时域与频域分别使用独立码表，给主模型提供预测目标。

- **NeuroDETR**：从连续信号构造多尺度时间 token 与脑区 token，作为事件检测的输入记忆。

- **DELTA**：按阅读词语组织 EEG 特征，用 RVQ 得到离散 token，再接入语言模型。

**把异构信号规则切段，统一成连续 token**：好处是 tokenizer 免训练、时域信息保留，坏处是 token 只是切分的产物，没有数据驱动的词表，谈不上语义单元；

**词表用在哪里**：

- **LaBraM**：离散 token 作为预训练目标，分类时保留主模型。

- **NeuroLM**：把离散 token 并入 GPT-2 词表，用指令组织下游任务。

- **TFM**：离散 token 作为主模型输入，tokenizer 可以接入不同骨干。

- **DELTA**：离散 token 作为 EEG-to-Text 的条件输入，由语言模型生成文本。

## 切分token方法的加固与新形态

- **CBraMod、LUNA · 时频双分支 + 位置编码**：

    每个 patch 的 embedding 由时域、频域两路相加而成，然后再单独编码通道结构；

- **EEGMoE**：token 单位不是波形段而是「时刻 × 频带 × 电极网格」的脑地图体素；


## token embedding 组成对比

| 论文 | 时域 | 频域 | 空间/通道 | 时间位置 |
|---|---|---|---|---|
| BIOT | — | STFT 幅值 → 线性投影 | 可学习通道表 | 正弦相对位置编码 |
| LaBraM / NeuroLM | temporal conv | 重构目标，不进 token | 10-20 空间表 | 可学习时间表 |
| EEGPT | patch embedding | 无显式 | 通道 codex book | predictor 内 RoPE |
| TFM | 线性投影 + GeLU | **频率 patch →  Transformer → 门控聚合** | 单通道，下游加通道 embedding | **tokenizer 内无** |
| CBraMod | 3 层 1D conv | FFT 能量 → FC | 并入 ACPE 卷积 | 并入 ACPE 卷积 |
| LUNA | 1D conv | FFT 幅度 + 相位 → MLP | 3D 坐标 NeRF 编码 | RoPE（时间 Transformer） |
| NeuroRVQ | 多尺度卷积 | 幅值 + 相位作重构目标 | 通道 embedding | 时间 embedding |
| BrainRVQ | patch 卷积 + Transformer | 幅值 + 相位作重构目标 | 通道位置 embedding | 时间位置编码 |
| CodeBrain | 时域卷积 | 频域卷积 | tokenizer 无通道标识，主模型 ACPE | tokenizer 时间 embedding |
| NeuroDETR | 连续信号卷积骨干 | 无显式频域输入 | 电极坐标混合 + 脑区分组 | 正弦位置编码 |


- **CBraMod / LUNA**：把时域与频域特征合成信号 embedding。

- **LaBraM / NeuroRVQ / BrainRVQ**：用频谱信息训练词表，频谱也是重构目标。

- **CodeBrain**：输入与词表重构均使用频域信息。

## 关键技术分歧

### 频域信息怎么进 token

| 方案 | 做法 | 问题 |
|---|---|---|
| BIOT | STFT 频谱帧 → 线性投影 | 丢失相位；1s 窗过粗，时域任务（P300）吃亏 |
| LaBraM | DFT 幅值+相位作重构目标 | 相位贡献小（NeuroLM 实验证实） |
| NeuroLM | 时域信号 + DFT 幅值双 decoder | — |
| TFM | 频率轴切 patch + 频率 Transformer + 门控聚合 | **显式建模窗内跨频段依赖**，最彻底 |
| CBraMod | rFFT 能量与时域 conv 相加进 embedding | 消融：时+频 > 纯时 > 纯频 |
| LUNA | FFT 幅相经 MLP 与时域 conv 相加 | 消融：**去掉后掉分最多的组件**（AUROC 至 -0.011） |
| NeuroRVQ | 重构对数幅值与相位，反变换后约束原始信号 | 用圆周相位损失处理角度周期性 |
| BrainRVQ | 独立频域 RVQ，重构幅值 + 相位 | 与时域 RVQ 分开保留两类信息 |
| CodeBrain | 频域卷积作为输入，独立频域码表重构幅值 + 相位 | 输入与重构目标都显式使用频域信息 |


## 遗留问题和可改进

- **固定窗长的软肋**：大 pattern 可能跨窗被切断，同一事件分到不同 token；

    采用Multi-scale patch输入，多尺度重建损失。

- **与自然语言对齐**：LaBraM/NeuroLM 都展望过把神经码与语言词汇对齐。

## 相关前端与解码方式

- **[LTFT](../papers/learnable-tf.md)**：直接学习时频变换的窗口，输出时频图；前端与下游网络一起训练，不建立离散码表。

- **[GUIDED](../papers/guided.md)**：用通道注意力与时空卷积把 EEG 编码为信号 embedding，再投影到 CLIP 图像表示空间，不建立离散码表。

- **[Défossez](../papers/defossez-speech.md)**：连续卷积提取脑信号表示，对齐语音模型的 embedding。

- **[SSM2Mel](../papers/ssm2mel.md)**：连续 EEG 特征经过状态空间模型与注意力，输出 mel 时频图。这里时频图是预测目标。

LTFT 学时频变换，TFM 在时频图上学离散词表，前端变换与词表训练需要分开看。

## 关联论文

[BIOT](../papers/biot.md) · [LaBraM](../papers/labram.md) · [EEGPT](../papers/eegpt.md) · [NeuroLM](../papers/neurolm.md) · [TFM-Tokenizer](../papers/tfm-tokenizer.md) · [CBraMod](../papers/cbramod.md) · [LUNA](../papers/luna.md) · [EEGDM](../papers/eegdm.md) · [JET](../papers/jet.md) · [EEGMoE](../papers/eegmoe.md) · [RF-GPT](../papers/rf-gpt.md) · [NeuroRVQ](../papers/neurorvq.md) · [BrainRVQ](../papers/brainrvq.md) · [CodeBrain](../papers/codebrain.md) · [NeuroDETR](../papers/neurodetr.md) · [DELTA](../papers/delta.md)

新增论文原文：[DELTA](https://arxiv.org/abs/2511.21746)（NeurIPS 2025 Workshop）。
