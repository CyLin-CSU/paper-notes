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
| REVE | OpenNeuro、MOABB、TUH、PhysioNet 等 92 个数据集 | **超过 61415h，24274 名被试** | 临床为主（约 50581h），混合认知与 BCI，396 个电极名 |
| EEGMoE | DREAMER、SEED、MAHNOB、EEGMMIDB、BCIC-IV-1、EEGMat | **6 个数据集，约 142h** | 情绪、运动想象、认知负荷 |
| NeuroRVQ | 12 个公开 EEG 数据集 + 自采运动数据 | **13 个来源**；自采部分约 **235h**，总时长未统一报告 | 运动、ERP、静息、伪迹、临床 |
| BrainRVQ | 清洗后的 TUEG | **约 9200h，1109545 个 30s 片段** | 临床 |
| CodeBrain | 清洗后的 TUEG | **约 9246h，1109545 个 30s 片段** | 临床 |
| NeuroDETR | BI2013a、BI2014b、Broderick、BNCI 系、HDOP、TUSZ | **8 个监督训练与评测数据集**，无独立通用预训练语料 | P300、语音、运动想象、运动执行、癫痫 |

BIOT 这里列的是无监督预训练的 EEG 数据；ECG 与跨数据集监督训练属于其他实验设定，不计入这 1000 万片段。

- **NeuroRVQ**：另有 ECG / EMG 数据，本表只列 EEG，各模态分别训练。

- **NeuroDETR**：列的是监督事件检测数据，没有独立通用预训练语料。

- **BrainRVQ**：报告约 9200h 清洗后的 TUEG。

- **REVE**：清洗哲学与 CBraMod 相反——不剔除 >100µV 段，只删 <10s 短记录与下游任务数据（防泄漏）。

- **CodeBrain**：报告约 9246h 清洗后的 TUEG。小时数按各自原文保留。



## 配对数据与评测数据

| 论文 | 数据来源 | 数据用途 |
|---|---|---|
| [Défossez](../papers/defossez-speech.md) | 4 个脑信号–语音配对数据集，含 EEG 与 MEG | 训练语音表示对齐，评测候选检索 |
| [SSM2Mel](../papers/ssm2mel.md) | SparrKULee | 监督训练 EEG 到 mel 时频图的映射 |
| [DELTA](../papers/delta.md) | ZuCo 1.0 + 2.0 | 训练词级 EEG tokenizer，适配文本生成模型 |
| [GUIDED](../papers/guided.md) | THINGS-EEG；另验证 MEG 迁移 | 训练脑信号与图像表示的对齐 |
| [CrossPT-EEG](../papers/crosspt-eeg.md) | 16 位被试的视觉 EEG，包含两阶段采集 | 跨被试、跨时间评测 |
| [EEGArena](../papers/eegarena.md) | 23 个公开数据集，构成 57 个下游任务 | 统一比较模型与训练协议 |

- **DELTA**：tokenizer 与语言模型的 EEG 适配均使用 ZuCo 训练数据，不把它计为额外的大规模通用语料。

- **CrossPT-EEG**：两阶段记录用于区分跨被试和跨时间迁移。

- **EEGArena**：数据规模指评测覆盖面，不表示所有模型共同使用这些数据预训练。

- **[LTFT](../papers/learnable-tf.md)**：在监督任务中学习时频前端，没有单列通用预训练语料。

- **[NPI](../papers/surrogate-brain.md)**：使用 fMRI 训练代理脑并做虚拟扰动，单独作为有效连接方法参考，不计入 EEG 数据规模。

### 关联论文

[BIOT](../papers/biot.md) · [LaBraM](../papers/labram.md) · [EEGPT](../papers/eegpt.md) · [BrainGPT](../papers/braingpt.md) · [NeuroLM](../papers/neurolm.md) · [TFM](../papers/tfm-tokenizer.md) · [CBraMod](../papers/cbramod.md) · [LUNA](../papers/luna.md) · [EEGMoE](../papers/eegmoe.md)

[数据集索引](../datasets.md) · [预训练范式对比](pretraining.md) · [通道适配与多任务学习](multi-task.md) · [十四篇方法对比](../comparison.md)

新增论文原文：[NeuroRVQ](https://arxiv.org/abs/2510.13068) · [BrainRVQ](https://arxiv.org/abs/2602.16951) · [CodeBrain](https://arxiv.org/abs/2506.09110) · [NeuroDETR](https://arxiv.org/abs/2610.20349)。
