---
title: 数据集索引
tags: [索引, 数据集]
---

# 数据集索引

六篇精读论文用到的全部数据集汇总。**↑ = 预训练语料，↓ = 下游评估**。同一数据集在不同论文中命名可能不同，见底部[别名说明](#别名说明)。

## 临床 EEG（Temple 大学 TUEG 体系）

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **TUEG** | 临床 EEG 语料 | 17–23ch / 250–1024Hz | ~24,000h | NeuroLM↑ |
| **TUAB** | 异常检测（二分类） | 23ch / 256Hz / 10s | 409,455 样本 | BIOT↓ LaBraM↓ NeuroLM↓ EEGPT↓ TFM↓ |
| **TUEV** | 事件分类（6 类） | 23ch / 256Hz / 5s | 112,491 样本 | BIOT↓ LaBraM↓ NeuroLM↓ EEGPT↓ TFM↓ |
| **TUSL** | 慢波分类（3 类） | 23ch / 256Hz / 10s | 245 样本 | NeuroLM↓ · LaBraM↑ |
| **TUSZ** | 癫痫事件检测 | 19–23ch / 256Hz | 1,138.5h | LaBraM↑ NeuroLM↑ |
| **TUEP** | 癫痫/非癫痫 | 19–23ch / 256Hz | 591.2h | LaBraM↑ NeuroLM↑ |
| **TUAR** | 伪迹标注（5 类） | 23ch / 256Hz | 92.2h | LaBraM↑ NeuroLM↑ |

## 情绪识别

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **SEED** | 3 类情绪 | 62ch / 1000Hz | 15 被试 | NeuroLM↓ · EEGPT↑ LaBraM↑ NeuroLM↑ |
| **SEED-IV** | 4 类情绪 | 62ch / 1000Hz | 15 被试 | BrainGPT↓ · LaBraM↑ NeuroLM↑ |
| **SEED-V** | 5 类情绪 | 62ch / 1000Hz | 20 被试 | LaBraM↓ BrainGPT↓ |
| **DEAP** | 情绪 (4 类) | 32ch / 128Hz | 32 被试 | BrainGPT↓ |
| **FACED** | 9 类情绪 | 30ch / 1000Hz | 123 被试 | BrainGPT↓ |
| **Emobrain** | 情绪 (IAPS 诱发) | 64ch / 1024Hz | 16 被试 | LaBraM↑ NeuroLM↑ |

## 运动想象 / 执行

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **PhysioMI**（EEG Motor Movement/Imagery） | MI & ME | 64ch / 160Hz | 109 被试 | EEGPT↑ LaBraM↑ NeuroLM↑ |
| **HGD** | MI（4 类） | 128ch | 14 被试 | EEGPT↑ |
| **MIBCI** | MI（2 类） | 64ch / 512Hz | 52 被试 | BrainGPT↓ |
| **BCI Competition IV-1**（BCIC4-1） | MI（2 类+空闲） | 38–59ch / 100Hz | 7 被试 | BrainGPT↓ · LaBraM↑ NeuroLM↑ |
| **Grasp and Lift** | 抓握动作 | 32ch / 500Hz | 12 被试 | LaBraM↑ NeuroLM↑ |

## 睡眠分期

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **SHHS** | 睡眠分期 | 2ch / 125Hz / 30s | 5,445 录音（500 万样本） | BIOT↑ |
| **EDF** | 睡眠分期（5 类） | 2ch / 100Hz | 78 晚 | BrainGPT↓ |
| **HMC** | 睡眠分期（5 类） | 4ch / 256Hz / 30s | 151 被试 | NeuroLM↓ BrainGPT↓ |
| **EESM23** | **ear-EEG** 睡眠分期 | 4ch（耳道电极） | 10 被试 | TFM 跨设备评估 |

## 认知负荷

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **EEGMat**（NeuroLM 中称 Workload） | 高/低认知负荷 | 19ch / 500Hz | 36 被试 | NeuroLM↓ BrainGPT↓ |
| **STEW** | 负荷（3 类） | 14ch / 128Hz | 45 被试 | BrainGPT↓ |

## ERP / P300 / SSVEP

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **Inria BCI** | P300 拼写 | 56ch / 600Hz | 26 被试 | LaBraM↑ NeuroLM↑ |
| **Target vs Non-Target** | P300 oddball | 32ch / 512Hz | 50 被试 | LaBraM↑ NeuroLM↑ |
| **PhysioP300** | P300 目标检测 | — | 9 被试 | EEGPT↓ |
| **KaggleERN** | 错误相关负电位 ERN | 56ch | 26 被试 | EEGPT↓ |
| **TSU** | SSVEP（40 目标） | 64ch / 250Hz | 35 被试 | EEGPT↑ |
| **M3CV** | 多范式生物识别 | — | 106 被试 | EEGPT↑ |

## ECG / 可穿戴 / 跨模态 / 其他

| 数据集 | 任务 | 配置 | 规模 | 使用情况 |
|---|---|---|---|---|
| **PTB-XL** | ECG 心律失常（二分类） | 12 导联 / 500Hz | 21,911 录音 | BIOT↓ |
| **Cardiology（5 套合集）** | ECG | 6/12 导联 / 500Hz | 21,264 录音 | BIOT↑ |
| **HAR** | 可穿戴 IMU 动作（6 类） | 9 坐标 / 50Hz | 30 被试 | BIOT↓ |
| **MoBI** | 步态关节角回归 | 60ch / 100Hz | 8 被试 | LaBraM↓ |
| **Raw EEG Data**（Trujillo 2020） | 信息整合分类 | 64ch / 256Hz | — | LaBraM↑ NeuroLM↑ |
| **Resting State**（Trujillo 2017） | 静息态 | 64ch / 256Hz | 22 被试 | LaBraM↑ NeuroLM↑ |
| **Siena Scalp** | 临床 EEG | 31ch / 512Hz | 14 患者 | LaBraM↑ NeuroLM↑ |
| **SPIS** | 静息+持续注意 | 64ch / 2048Hz | 10 被试 | LaBraM↑ NeuroLM↑ |
| **Self-collected** | 混合任务 | 62ch / 1000Hz | 140+ 被试 | LaBraM↑ NeuroLM↑ |
| **DREAMER** | 情绪（预训练未见） | — | 23 被试 | BrainGPT 迁移性验证 |

## 别名说明

| 别名 | 指向 |
|---|---|
| EEGMat = Workload | 同一数据集（Zyma et al. 2019 心算范式），BrainGPT 称 EEGMat、NeuroLM 称 Workload |
| BCI Competition IV-1 = BCIC4-1 | 同一数据集（Blankertz et al. 2007） |
| PhysioMI = EEG Motor Movement/Imagery Dataset | PhysioNet 上的 BCI2000 采集数据（Schalk et al. 2004） |
| SEED 系列 | SEED / SEED-IV / SEED-V / SEED-GER / SEED-FRA 的统称 |
| EDF | Sleep-EDFx 数据库的子集（Kemp et al. 2000），BrainGPT 基准中称 EDF |
