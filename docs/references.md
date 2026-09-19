---
title: 参考文献索引
tags: [索引, 参考文献]
---

# 参考文献索引

六篇精读论文引用的关键文献，按主题分类。"被引于"标注了哪些精读论文用到它。

## 基础架构与预训练范式

| 文献 | 出处 | 被引于 | 一句话作用 |
|---|---|---|---|
| An Image is Worth 16x16 Words (ViT) | ICLR 2021 | BIOT · LaBraM · EEGPT | patch 化输入思想，BIOT/LaBraM 切段的直接灵感 |
| BERT | NAACL 2019 | LaBraM · EEGPT · NeuroLM | 掩码重建预训练范式的源头 |
| BEiT | ICLR 2022 | LaBraM · NeuroLM | "先训 tokenizer 再做 BERT 式预训练"的直接模板 |
| BEiT v2 | arXiv 2022 | LaBraM · NeuroLM | ℓ2 归一化查表提升 codebook 利用率的技术出处 |
| MAE | CVPR 2022 | BrainGPT · EEGPT | 掩码自编码器的代表，被 BrainGPT 用作 AR 的对照组 |
| GPT 系列通用范式 | 2018–2020 | LaBraM · BrainGPT · NeuroLM | 自回归下一 token 预测 |
| GPT-2 | OpenAI 2019 | NeuroLM | NeuroLM 的基座语言模型 |
| ViT-22B 训练修改 | ICML 2023 | LaBraM | QK 先 LayerNorm、QKV 去 bias 等稳定化技巧 |

## 注意力与效率组件

| 文献 | 出处 | 被引于 | 一句话作用 |
|---|---|---|---|
| Linformer | arXiv 2020 | BIOT | 低秩 E/F 投影线性注意力的出处 |
| Transformers are RNNs（线性注意力） | ICML 2020 | BIOT · TFM | 线性复杂度注意力的另一条路线；TFM 下游直接采用 |
| Graph Attention Networks (GAT) | ICLR 2018 | BrainGPT | TEG 电极图网络的注意力机制 |
| RoFormer（RoPE 旋转位置编码） | NeuroComputing 2024 | EEGPT | predictor 的时间位置信息 |
| LayerNorm | arXiv 2016 | 全部六篇 | 各处归一化的基础组件 |
| GroupNorm | ECCV 2018 | LaBraM | temporal encoder 卷积块内的归一化 |
| Swish / 门控线性单元 | ICML 2017 | BrainGPT | ETE 前馈网络的 Swish 激活（公式为门控形式） |

## 自监督与表征学习理论

| 文献 | 出处 | 被引于 | 一句话作用 |
|---|---|---|---|
| VQ-VAE | NeurIPS 2017 | LaBraM · NeuroLM · TFM | 连续信号离散化为码字的量化框架 |
| BYOL | NeurIPS 2020 | BIOT · EEGPT | 无负样本对比/动量目标 + predictor 的自监督设计 |
| MoCo | CVPR 2020 | BIOT | 动量编码器对比学习 |
| SimCLR | ICML 2020 | BIOT | 对比损失形式（CrossEntropy+温度） |
| CLIP | ICML 2021 | NeuroLM | 视觉-文本 embedding 对齐的参照（NeuroLM 说明为何不能照搬） |
| DANN（梯度反转层 GRL） | JMLR 2016 | NeuroLM | EEG-文本空间对齐的对抗机制 |
| Auto-Encoding Variational Bayes（VAE） | ICLR 2014 | LaBraM · NeuroLM | 两段式训练的 ELBO 理论解释 |
| wav2vec 2.0 | NeurIPS 2020 | LaBraM · EEGPT | 语音域掩码+对比自监督；BENDR 的底座 |
| Scaling Laws for Neural Language Models | arXiv 2020 | LaBraM · BrainGPT · EEGPT | 模型/数据规模实验的理论依据 |
| MVEB 多视图熵瓶颈 | TPAMI 2024 | EEGPT | "最小充分表示"动机的出处 |
| Formal Algorithms for Transformers | arXiv 2022 | EEGPT | embedding/unembedding 术语与实现参照 |

## EEG 领域先前模型与基线

| 文献 | 出处 | 被引于 | 一句话作用 |
|---|---|---|---|
| EEGNet | JNE 2018 | BrainGPT | 紧凑卷积基线（w/o pre-train 组） |
| BENDR | Front. Hum. Neurosci. 2021 | LaBraM · EEGPT | 最早的 EEG 大规模自监督模型之一，wav2vec 2.0 适配 |
| ContraWR | JMIR AI 2023 | BIOT · LaBraM · EEGPT · NeuroLM · TFM | 世界表征对比的睡眠分期自监督方法（BIOT 作者自引） |
| SPaRCNet | Neurology 2023 | BIOT · LaBraM · EEGPT · NeuroLM · TFM | 1D-CNN 密集残差连接，临床 EEG 基线 |
| CNN-Transformer | EMBC 2022 | BIOT · LaBraM · EEGPT · TFM | 卷积+Transformer 混合基线 |
| FFCL | BSPC 2022 | BIOT · LaBraM · EEGPT · NeuroLM · TFM | CNN+LSTM 特征融合基线 |
| ST-Transformer | arXiv 2021 | BIOT · LaBraM · EEGPT · NeuroLM · TFM | 空间-时间多级 Transformer 基线 |
| BrainBERT | ICLR 2023 | LaBraM | 颅内 SEEG 频谱掩码自监督（43.6h 小数据先行者） |
| neuro2vec | arXiv 2022 | LaBraM | 掩码傅里叶频谱预测的思想来源 |
| MMM | NeurIPS 2023/2024 | NeuroLM · TFM | 拓扑无关表示（多维位置编码、多级通道层次） |
| Brant | NeurIPS 2023 | NeuroLM | 颅内 EEG 基础模型（长程依赖+时空联合） |
| CBraMod | arXiv 2024 | TFM | 跨颅脑基础模型（TFM 的多数据集对照组） |
| DeWave | NeurIPS 2023 | EEGPT | 离散 EEG 编码词表（Codex book 概念出处） |
| EEG2VEC | arXiv 2023 | EEGPT | 对比+重构损失学习 EEG 表示的相关工作 |

## 信号处理基础

| 文献 | 出处 | 被引于 | 一句话作用 |
|---|---|---|---|
| Nyquist (1928) / Shannon (1949) | 经典 | BIOT | 重采样率选取（≥2× 最高关注频率）的理论依据 |
| EMD / Hilbert 谱 | Royal Soc. 1998 | TFM | 时域信号频率成分纠缠（频率坍缩）讨论的起点 |
| Frequency Principle | Comm. Comp. Phys. 2020 | TFM | 神经网络偏重低频、忽略高频的理论依据 |
