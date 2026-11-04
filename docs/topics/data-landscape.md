---
title: EEG 预训练数据全景
tags: [预训练数据, 综述]
---


## 预训练数据

| 论文 | 数据来源 | 报告规模 | 数据类型 |
|---|---|---|---|
| BIOT | PREST + SHHS | **约 1000 万多通道片段** | 静息、睡眠 |
| LaBraM | TUSZ、TUEP 等约 20 个数据集 | **约 2500h** | 以临床数据为主，混合其他任务 |
| EEGPT | PhysioMI、HGD、TSU、SEED、M3CV | **5 个数据集** | 运动想象、SSVEP、情绪、多任务 |
| BrainGPT | 12 个基准的预训练拆分 | **3750 万单通道片段，约 10 亿 token** | 情绪、运动想象、认知负荷、睡眠等 |
| NeuroLM | TUEG 为主，混合其他公开数据集 | **约 25000h** | 以临床数据为主，混合其他任务 |
| TFM | TUEV、TUAB、CHB-MIT、IIIC | **4 个数据集**，含单数据集与多数据集设定 | 临床事件、异常、癫痫 |
| CBraMod | 清洗后的 TUEG | **超过 9000h，约 110 万个 30s 片段** | 临床 |
| LUNA | TUEG + Siena | **超过 21900h** | 临床，覆盖多种电极布局 |
| EEGMoE | DREAMER、SEED、MAHNOB、EEGMMIDB、BCIC-IV-1、EEGMat | **6 个数据集，约 142h** | 情绪、运动想象、认知负荷 |
| NeuroRVQ | 12 个公开 EEG 数据集 + 自采运动数据 | **13 个来源**；自采部分约 **235h**，总时长未统一报告 | 运动、ERP、静息、伪迹、临床 |
| BrainRVQ | 清洗后的 TUEG | **约 9200h，1109545 个 30s 片段** | 临床 |
| CodeBrain | 清洗后的 TUEG | **约 9246h，1109545 个 30s 片段** | 临床 |
| NeuroDETR | BI2013a、BI2014b、Broderick、BNCI 系、HDOP、TUSZ | **8 个监督训练与评测数据集**，无独立通用预训练语料 | P300、语音、运动想象、运动执行、癫痫 |

BIOT 这里列的是无监督预训练的 EEG 数据；ECG 与跨数据集监督训练属于其他实验设定，不计入这 1000 万片段。

NeuroRVQ 另有 ECG / EMG 数据，本表只列 EEG；NeuroDETR 列的是监督任务数据，不与其他方法的预训练规模直接比较。BrainRVQ 与 CodeBrain 的小时数为各自原文的近似口径。



### 关联论文

[BIOT](../papers/0918-biot.md) · [LaBraM](../papers/0918-labram.md) · [EEGPT](../papers/0918-eegpt.md) · [BrainGPT](../papers/0918-braingpt.md) · [NeuroLM](../papers/0918-neurolm.md) · [TFM](../papers/0918-tfm-tokenizer.md) · [CBraMod](../papers/0928-cbramod.md) · [LUNA](../papers/0924-luna.md) · [EEGMoE](../papers/0924-eegmoe.md)

[数据集索引](../datasets.md) · [预训练范式对比](pretraining.md) · [通道适配与多任务学习](multi-task.md) · [十三篇方法对比](../comparison.md)

新增论文原文：[NeuroRVQ](https://arxiv.org/abs/2510.13068) · [BrainRVQ](https://arxiv.org/abs/2602.16951) · [CodeBrain](https://arxiv.org/abs/2506.09110) · [NeuroDETR](https://arxiv.org/abs/2610.20349)。
