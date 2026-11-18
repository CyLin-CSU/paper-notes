---
date: 2026-11-18
title: "EEG foundation models: a critical review of current progress and future directions"
authors: [Gayal Kuruppu, Neeraj Wagh, Vaclav Kremen, Yogatheesan Varatharajah]
venue: "J. Neural Eng. 2026"
year: 2026
tags: [综述, 批判性综述, 评测, scaling, 线性探针, OOD]
status: "精读"
rating: 4.5
doi: "10.1088/1741-2552/ae4455"
arxiv: ""
code: "https://github.com/gayalkuruppu/eeg-foundation-models"
one-liner: "三支柱拆 10 个早期 EEG FM 后给出批判性结论：评测异质且多在分布内、scaling 证据弱、线性探针明显落后微调——SSL 表示质量存疑"
---

# EEG foundation models: a critical review of current progress and future directions

> **J. Neural Eng. 23, 021001（2026）· Topical Review · Open Access**

**作者**：Gayal Kuruppu、Neeraj Wagh（共同一作；UMN / UIUC）、Vaclav Kremen（Mayo Clinic）、Yogatheesan Varatharajah（通讯，UMN / Mayo Clinic）

## 1 问题定位

同期的综述（作者点名 Yao et al. 2025 等）偏技术组件（架构、SSL 策略），这篇自称补位的是**数据与领域视角**：早期 EEG FM 的真实成熟度、可长期追踪的评判标准。检索 2021-01–2024-09，收录 10 个 FM：BrainBERT、Neuro-GPT、Brant、BIOT、EEGFormer、LaBraM、Mentality（Mamba）、NeuroLM、FoME、BrainWave；多模态与 PSG 睡眠 FM 明确排除。数据规模用 **channel-hours** 口径（时长 × 通道数）：BrainBERT 4.5k → BrainWave 878k，TUEG 单库 541k。与其他综述的「小时数」口径不可直接互比。

## 2 十模型概要（原 Table 1 复现）

| 模型 | 预训练数据（channel-hours） | 参数量 | 输入配置 | 数据类型 | 架构组件 | SSL 任务 |
|---|---|---|---|---|---|---|
| BrainBERT | 4.5k | 43.18M | 单通道谱图 | iEEG | Transformer encoder + 两层线性浅 decoder | 掩码重构（STFT/Superlet 谱图） |
| Neuro-GPT | 541k | 79.53M | 固定多通道时序（10-20 布局 22 导） | 头皮 EEG | conv+Transformer encoder + GPT-2 decoder | 掩码重构（隐变量因果掩码） |
| Brant | 281k | 68M / 104M / 249M / 506M | 变通道时序 | iEEG | 时序 + 空间双 Transformer encoder + 线性 decoder | 掩码重构 |
| BIOT | 312k | 3.3M | 变通道谱数据（「biosignal sentences」） | 头皮 EEG | 线性 Transformer，encoder-only | 对比学习（SimCLR 式） |
| EEGFormer | 541k | — | 多通道谱数据 | 头皮 EEG | Transformer encoder + 浅 decoder | 码本式重构 |
| LaBraM | 80k | 5.8M / 46M / 369M | 固定多通道时序 | 头皮 EEG | conv 时序 encoder + Transformer + 线性 decoder（tokenizer 独立 decoder） | 掩码重构（token 级） |
| Mentality | — | — | 固定多通道时序 | 头皮 EEG | conv + Mamba 块（encoder 与 decoder） | 掩码重构 |
| NeuroLM | 546k | 250M / 500M / 1.7B | 变通道时序 | 头皮 EEG | VQ tokenizer + conv 时序 encoder + Transformer 空间 encoder | 自回归重构（token 级） |
| FoME | — | 476M / 745M | 变通道时序 | 头皮 + 颅内 | 时序 + 空间 Transformer encoder + 线性 decoder | 掩码信号重构 |
| BrainWave | 878k | — | 变通道谱图 | 头皮 + 颅内 | Transformer encoder + 通道注意力 + 轻量 decoder | 掩码重构（整谱图） |

模型间有三个数量级跨度值得注意：数据量 4.5k → 878k channel-hours（约 200 倍）、参数 3.3M（BIOT）→ 1.7B（NeuroLM，约 500 倍）、模态组合（纯头皮 6 / 纯颅内 2 / 双模态 2）。Mentality 两栏未报是该综述自己标注的数据缺口。

## 3 三支柱对比

**支柱一：输入表示**。多元时序 6/10（借此适配变通道：Brant、NeuroLM、FoME 等）；功率谱 2/10（BIOT、EEGFormer）；时域+谱双输入 2/10（Brant、FoME）；时频表示 2/10（BrainBERT、BrainWave）。

切段与上下文长度（§4.2 整理）：

| 模型 | patch 粒度 | 上下文长度 |
|---|---|---|
| Brant / FoME | 6 s | FoME 90 s（15 token） |
| BrainBERT | 5 s（STFT/Superlet 窗） | — |
| Neuro-GPT | 2 s（重叠） | 32 token ≈ 57.8 s |
| LaBraM / NeuroLM / BIOT / BrainWave | 1 s | LaBraM 至 256 token；BIOT 19 token/通道；EEGFormer 12 s |

掩码策略（§4.2 整理）：

| 模型 | 掩码方式 |
|---|---|
| Brant / FoME | ~40% 均匀随机（时空两维零化） |
| LaBraM | 50% patch 级 |
| BrainBERT | 时域 5% + 频域 5%（总 ~10%，最细粒度） |
| BrainWave | 掩整幅多通道谱图 |
| Mentality | 随机整通道掩码 |
| NeuroLM | 阶梯式通道条件自回归 |
| Neuro-GPT | 隐空间因果掩码 |

空间编码谱系（§4.2）：Brant / FoME 靠空间注意力但不加空间 PE；LaBraM / BIOT / NeuroLM 显式空间编码（其中仅 BIOT 支持多配置，LaBraM/NeuroLM 绑定 10-20）；Neuro-GPT / Mentality 卷积隐式学空间；BrainWave 空间注意力；BrainBERT / EEGFormer 完全不做空间建模。

**支柱二：建模与 SSL**。7/10 用掩码时序重构；只有 Neuro-GPT 在隐空间做因果掩码重构；BIOT 用 SimCLR 式对比；NeuroLM 通道条件阶梯式自回归。码本一族（LaBraM、NeuroLM、EEGFormer）用 VQ-VAE 式 tokenizer，用途各异——LaBraM 拿码字当重构目标、NeuroLM 接文本词表、EEGFormer 拿码本做可解释归因。

**支柱三：评测**。逐模型覆盖：

| 模型 | 评测任务数 | 与预训练数据的关系 | 适配方式 | OOD |
|---|---|---|---|---|
| BrainBERT | 1（Brain TreeBank 电影特征） | 同分布 | FT + LP | ✗ |
| Neuro-GPT | 1（四类 MI，转换到 10-20 布局） | 外部数据 | FT + LP | ✓ |
| Brant | 4 类任务 × 3 个未见 iEEG 数据集（MAYO/FNUSA/私有） | OOD | FT + LP | ✓ |
| BIOT | 4（CHB-MIT、TUAB、IIIC、TUEV） | 未见数据 | FT | 部分 |
| EEGFormer | 5（TUH 系）+ 新生儿癫痫 OOD | 部分重叠 | FT | ✓（新生儿） |
| LaBraM | 4（TUAB/TUEV/SEED-V/MoBI），MoBI 唯一外部 | 部分重叠 | FT | 部分 |
| Mentality | 1（TUSZ） | 同分布 | LP | ✗ |
| NeuroLM | 6 任务联合微调 | 部分重叠 | 指令微调 | ✗ |
| FoME | 7 任务 × 4 数据集 | 同分布 | FT | ✗ |
| BrainWave | 12（跨被试/跨医院/跨亚型/few-shot） | OOD | few-shot 原型 | ✓ |

汇总读法：任务数 1（Mentality）到 12（BrainWave），多数 ≤5；4/10 在分布内评测；**只有 BrainWave 和 Brant 做过真正的 OOD 评测**。共享任务只有 TUAB 与 TUEV（4 个模型可比）：TUAB AUC 0.86–0.92、TUEV F1 0.70–0.83；文中引证据说 TUAB 用传统方法已到 85–87% 精度，属饱和任务。linear probing 结果只有 LaBraM 报了（图 3 三角标）。

## 4 批判性结论（§5 的干货）

- **Scaling 证据弱**：预训练数据规模与 TUAB/TUEV 性能无正相关（LaBraM 数据最多却与 EEGFormer/NeuroLM 互有胜负）；LaBraM 自家曲线 ~1000 h 后趋平；模型缩放（3.3M–1.7B）只有边际改进。
- **线性探针显著落后微调**：五个报告 LP 的模型全线弱于 FT 与部分监督基线；FT 又略胜从头监督——作者据此**质疑 SSL 学到的表示质量**：增益可能主要来自架构与初始化而非预训练知识。
- **通用时序 FM 意外能打**：PatchTST / TimesNet 微调后在病理检测、睡眠分期可打平甚至超过 EEG FM；BrainWave 的实验里 MOMENT 在癫痫检测与病理检测超过 EEG FM。EEG 专属归纳偏置（空间建模、头皮+颅内联合）是 EEG FM 的反超点。
- **预处理普遍极简**：无显式去伪迹、归一化策略多数语焉不详，对 OOD 的影响未知。
- **数据多样性 vs 数据量**：LaBraM 在 TUAB/TUEV 的领先可能来自数据源多样性（source 数）而非 channel-hours 绝对量；BrainWave 的头皮+颅内联合消融显示联合预训练几乎全面优于单模态。

## 5 消融与可解释性补充（§4.3 末）

逐模型消融中的可复用结论：Neuro-GPT 去掉 GPT decoder 反而提升下游（decoder 只服务预训练）；Brant 消融显示时序 encoder 贡献最大；LaBraM 空间 embedding 对预训练收敛与下游都关键、码本对 TUEV 这类复杂任务必要；NeuroLM 的 tokenizer 目标（频率/时序/双域）适配不同下游；BrainWave 头皮+颅内联合预训练除一项外全面占优。可解释性仅两例：BrainBERT 用内在维度（ID）分析电极表示、EEGFormer 用码本做癫痫归因（高亮区与棘波形态吻合）。

## 6 未来方向三主题

基准与工具（对照既有特征范式并给统计检验、社区标准基准、进国际竞赛、低摩擦软件）；技术（整体评测框架、联邦学习、多模态预训练、蒸馏/剪枝做小模型）；应用（模型卡辅助选型、临床阅片辅助、按 SaMD 监管路径落地）。

## 7 站内视角

- 本篇的批判清单与 [EEGArena](../survey/eegarena.md) 高度互补：文中呼吁的「共享核心任务 + OOD + 强监督基线」正是 EEGArena 已经做成的事，两篇可当「诊断书与药方」连读。
- LP 落后 FT 的观察对本站 [REVE](../fm/reve.md) 微调策略（缓存 LP → 小学习率 FT）是提醒而非定论：该综述纳入的线性探针结果与全量微调存在差距，涉及五个模型的不同任务与指标，比较时须注明各自任务与设定，外推为「EEG FM 的普遍规律」证据尚不足。
- 三支柱框架（输入表示 / 建模 / 评测）与本站 [预训练范式专题](../../topics/pretraining.md) 的「目标 / 掩码 / 范式」切分兼容，可交叉引用；§2 概要表与 [Yao 综述的设计总表](yao-eegfm-survey.md)、[Chen 综述的拆解表](chen-representation-learning-review.md) 三表字段口径不同，合读覆盖最全。

---

**相关阅读**

:material-sword-cross: [EEGArena（批判清单的落地实现）](../survey/eegarena.md) ｜ :material-format-list-bulleted: [Yao 综述（同刊前一年的技术面版本）](yao-eegfm-survey.md) ｜ :material-electric-bolt: [BrainGPT（文中 NeuroLM 的直接前身与对照）](../fm/braingpt.md) ｜ :material-tune: [REVE（LP/FT 差异与本站微调策略相关）](../fm/reve.md)
