---
title: EEG Tokenization 演进
tags: [tokenization, 综述]
---

# EEG Tokenization 演进

## 论文代码开源情况

| 论文 | 代码 | 备注 |
|---|---|---|
| [BIOT](../papers/0918-biot.md) | [ycq091044/BIOT](https://github.com/ycq091044/BIOT) | 完整开源 |
| [LaBraM](../papers/0918-labram.md) | [935963004/LaBraM](https://github.com/935963004/LaBraM) | 仅 Base 权重；Large / Huge 未放 |
| [EEGPT](../papers/0918-eegpt.md) | [BINE022/EEGPT](https://github.com/BINE022/EEGPT) | 开源 |
| [NeuroLM](../papers/0918-neurolm.md) | [935963004/NeuroLM](https://github.com/935963004/NeuroLM) | 开源 |
| [TFM-Tokenizer](../papers/0918-tfm-tokenizer.md) | [Jathurshan0330/TFM-Tokenizer](https://github.com/Jathurshan0330/TFM-Tokenizer) | 含预训练权重与全部预处理脚本 |
| [CBraMod](../papers/0928-cbramod.md) | [wjq-learning/CBraMod](https://github.com/wjq-learning/CBraMod) | 已进 Braindecode |
| [LUNA](../papers/0924-luna.md) | [pulp-bio/biofoundation](https://github.com/pulp-bio/biofoundation) | Base / Large / Huge 全系 |
| [EEGDM](../papers/1017-eegdm.md) | [wangsc18/EEGDM](https://github.com/wangsc18/EEGDM) | 含预处理脚本与训练配置 |
| [JET](../papers/0923-jet.md) | [项目页](https://y-research-sbu.github.io/JET/) | 代码 / 权重以项目页为准 |
| [EEGMoE](../papers/0924-eegmoe.md) | — | 论文声明将放出，精读时未见仓库 |
| [RF-GPT](../papers/0921-rf-gpt.md) | — | 论文未附仓库（底座 Qwen2.5-VL 等组件公开可得） |
| [NeuroRVQ](../papers/1104-neurorvq.md) | [项目页](https://neurorvq.github.io) · [Hugging Face](https://huggingface.co/ntinosbarmpas/NeuroRVQ) | 官方实现挂 HF（另有第三方 [Rust 推理](https://github.com/eugenehp/neurorvq-rs)） |
| [BrainRVQ](../papers/1104-brainrvq.md) | [keqicmz/BrainRVQ](https://github.com/keqicmz/BrainRVQ) | 代码可访问，权重承诺论文接收后放出 |
| [CodeBrain](../papers/1104-codebrain.md) | [jingyingma01/CodeBrain](https://github.com/jingyingma01/CodeBrain) | ICLR 2026 官方开源 |
| [NeuroDETR](../papers/1104-neurodetr.md) | — | 暂未检索到官方仓库 |
| [DELTA](../papers/1104-delta.md) | — | 论文未附仓库（NeurIPS 2025 Workshop） |

| 时间 | 论文 | Token 形态 | 词表 | Token 的用途 |
|---|---|---|---|---|
| 2023 | [BIOT](../papers/0918-biot.md) | 原始信号片段（1s） | 无 | 模型输入 |
| 2024 | [LaBraM](../papers/0918-labram.md) | 离散码（VQ，8192） | 有 | **仅作预训练目标**，推理时丢弃 |
| 2024 | [EEGPT](../papers/0918-eegpt.md) | 连续 patch embedding | 无 | 模型输入 |
| 2025 | [NeuroLM](../papers/0918-neurolm.md) | 离散码（VQ） | 有（并入 GPT-2 词表） | LLM 的输入 |
| 2026 | [TFM-Tokenizer](../papers/0918-tfm-tokenizer.md) | 离散码（VQ 时频 motif） | 有 | 模型输入 + 可插拔复用 |
| 2026 | [NeuroRVQ](../papers/1104-neurorvq.md) | 多尺度 RVQ 离散 token | 多尺度、多层码表 | 预训练目标 |
| 2026 | [BrainRVQ](../papers/1104-brainrvq.md) | 时域 / 频域双 RVQ 离散 token | 双域、多层码表 | 分层预训练目标 |
| 2026 | [CodeBrain](../papers/1104-codebrain.md) | 时域 / 频域双 VQ 离散 token | 双域码表 | 预训练目标 |
| 2026 | [NeuroDETR](../papers/1104-neurodetr.md) | 时间多尺度 / 空间金字塔离散 token | 时间 / 空间码表 | 事件检测模型的输入记忆 |
| 2025 | [DELTA](../papers/1104-delta.md) | RVQ 离散码（词级 EEG） | 自训多层码表 | 掩码语言扩散的输入 |

## 预处理与归一化异构信号

- **重采样**：BIOT / CBraMod / EEGDM / JET 统一 200Hz；EEGPT / LUNA 统一 256Hz。

    滤波：LUNA 0.1–75Hz 带通 + 50/60Hz 陷波，CBraMod 0.3–75Hz 带通 + 60Hz 陷波；
- **归一化的四种方式**：BIOT 逐通道除以绝对幅值 **95 分位数**；LUNA 逐通道 **z-score**；CBraMod 以 **100µV 为单位**归一；JET 幅值整体 **×0.01**。

## 片段细粒度

- **patch 时间长度**：

    LUNA 最细（40 个时间点，256Hz 约 0.16s），EEGPT 250ms（64 点）

    主流200点，在200Hz下 **1s** （BIOT / LaBraM / TFM / CBraMod / EEGDM / JET）

    粒度选择与「motif 通常持续亚秒到数秒」的生理直觉大体一致；
- **重叠与否**：BIOT 与 TFM 使用重叠窗口（0.5s）；BrainRVQ / CodeBrain 使用 1s 非重叠 patch。不同方法的切分口径单独记录；
- **切分对象**：主流「时域信号每通道独立切」；

    几个例外：**EEGMoE**，先分 5 个频带（δ 1–4 / θ 4–8 / α 8–14 / β 14–31 / γ 31–45Hz）、按头皮位置摆成 2-D 网格再堆成 4-D 脑地图 X ∈ R^{T×F×H×W}；**RF-GPT 把整个 STFT 时频图当一张 512×512 图片**切 14×14 patch（1369 个 token）。

## 对token切分的总结

**新增方法的切分**：NeuroRVQ 在 patch 内用多尺度卷积，再逐尺度做 RVQ；BrainRVQ 把同一 patch 分成时域 / 频域两组残差码字；CodeBrain 使用时域 / 频域双码表。NeuroDETR 从连续信号特征构造多尺度时间 token 与脑区 token，不按统一 1s patch 比较。

**把异构信号规则切段，统一成连续 token**：好处是 tokenizer 免训练、时域信息保留，坏处是 token 只是切分的产物，没有数据驱动的词表，谈不上语义单元；

**学神经词表**，LabraM的词表只当掩码预训练的目标、推理时被丢弃；到 NeuroLM 和 TFM——前者把码字并入 GPT-2 词表换来单模型多任务的指令推理，后者把时频 motif 词表做成可插拔组件。

## 切分token方法的加固与新形态

- **CBraMod、LUNA · 时频双分支 + 位置编码**：

    每个 patch 的 embedding 由时域、频域两路相加而成，然后再单独编码通道结构；

- **EEGMoE**：token 单位不是波形段而是「时刻 × 频带 × 电极网格」的脑地图体素；


## token embedding 组成对比

| 论文 | 时域 | 频域 | 空间/通道 | 时间位置 |
|---|---|---|---|---|
| BIOT | —（切段即 token） | FFT 能量 → FCN | 可学习通道表 | 正弦相对位置编码 |
| LaBraM / NeuroLM | temporal conv | 重构目标，不进 token | 10-20 空间表 | 可学习时间表 |
| EEGPT | patch embedding | 无显式 | 通道 codex book | predictor 内 RoPE |
| TFM | 线性投影 + GeLU | **频率 patch →  Transformer → 门控聚合** | 单通道，下游加通道 embedding | **tokenizer 内无** |
| CBraMod | 3 层 1D conv | FFT 能量 → FC | 并入 ACPE 卷积 | 并入 ACPE 卷积 |
| LUNA | 1D conv | FFT 幅度 + 相位 → MLP | 3D 坐标 NeRF 编码 | RoPE（时间 Transformer） |
| NeuroRVQ | 多尺度卷积 | 幅值 + 相位作重构目标 | 通道 embedding | 时间 embedding |
| BrainRVQ | patch 卷积 + Transformer | 幅值 + 相位作重构目标 | 通道位置 embedding | 时间位置编码 |
| CodeBrain | 时域卷积 | 频域卷积 | tokenizer 无通道标识，主模型 ACPE | tokenizer 时间 embedding |
| NeuroDETR | 连续信号卷积骨干 | 无显式频域输入 | 电极坐标混合 + 脑区分组 | 正弦位置编码 |


两个规律：频域几乎都以双分支相加/拼接的方式进入 embedding 层；空间与位置编码基本是查表，或者是动态可学习。

## 关键技术分歧

### 频域信息怎么进 token

| 方案 | 做法 | 问题 |
|---|---|---|
| BIOT | FFT 能量向量 → FCN | 丢失相位；1s 窗过粗，时域任务（P300）吃亏 |
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

## 关联论文

[BIOT](../papers/0918-biot.md) · [LaBraM](../papers/0918-labram.md) · [EEGPT](../papers/0918-eegpt.md) · [NeuroLM](../papers/0918-neurolm.md) · [TFM-Tokenizer](../papers/0918-tfm-tokenizer.md) · [CBraMod](../papers/0928-cbramod.md) · [LUNA](../papers/0924-luna.md) · [EEGDM](../papers/1017-eegdm.md) · [JET](../papers/0923-jet.md) · [EEGMoE](../papers/0924-eegmoe.md) · [RF-GPT](../papers/0921-rf-gpt.md) · [NeuroRVQ](../papers/1104-neurorvq.md) · [BrainRVQ](../papers/1104-brainrvq.md) · [CodeBrain](../papers/1104-codebrain.md) · [NeuroDETR](../papers/1104-neurodetr.md) · [DELTA](../papers/1104-delta.md)

新增论文原文：[DELTA](https://arxiv.org/abs/2511.21746)（NeurIPS 2025 Workshop）。
