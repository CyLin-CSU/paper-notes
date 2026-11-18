---
title: EEG 基础模型全景 · 2026-11
tags: [全景, 研究重点, 痛点, 空白轴, 综述]
---

# EEG 基础模型全景 · 2026-11

> 本文综合站内 31 篇精读与四篇领域综述（[Yao, JNE 2025](papers/reviews/yao-eegfm-survey.md) · [Chen, Lu & Wu, IEEE SPM 2025](papers/reviews/chen-representation-learning-review.md) · [Kuruppu et al., JNE 2026](papers/reviews/kuruppu-critical-review.md) · [Kwon & Shin, EJN 2026](papers/reviews/kwon-neural-fm-perspective.md)），给出研究重点、痛点、创新集中度与空白轴的全景判断。

**引用规则**：站内事实均带笔记或综述链接，并标注原文节号 / 表号；数字口径以各论文原文为准（channel-hours 与小时数不混用，见 [Kuruppu 综述](papers/reviews/kuruppu-critical-review.md) §1 的口径说明）。少数来自站外检索、站内尚未核对原文的动态集中在 §7，单独标注，不作为结论使用。标注「站内统计」的计数按本站笔记口径统计，一篇论文可占多个设计格。

## 1 领域现状一句话

**架构移植期已经结束，评测清算期刚刚开始。** 2021–2024 是把 BERT / MAE / GPT 范式搬进 EEG 的收编期（[Kuruppu 综述](papers/reviews/kuruppu-critical-review.md) §1：其收录的 10 个 FM 全部为 transformer 或 Mamba 骨干、7/10 用掩码重构）；2025–2026 的主线变成两件事：在移植过的骨架上卷组件差异（§2 的拥挤度），以及用统一评测反向拆台——[EEGArena](papers/survey/eegarena.md) 以 30 FM × 25 监督基线 × 57 任务给出「参数量不预测性能」（其 §3），[Yao 综述](papers/reviews/yao-eegfm-survey.md) §6 自跑显示 FM 在运动想象上不敌 0.003M 的 EEGNet。

## 2 研究重点：四条主线与拥挤度

站内 31 篇按设计轴归类（站内统计，可多格重复计入）：

| 主线 | 成员 | 拥挤度 |
|---|---|---|
| 连续 patch + 掩码重构 | [CBraMod](papers/fm/cbramod.md)、[LUNA](papers/fm/luna.md)、[REVE](papers/fm/reve.md)、[EEGMoE](papers/fm/eegmoe.md)、[Uni-NTFM](papers/fm/uni-ntfm.md)、[EEGPT](papers/fm/eegpt.md)（对齐+重构双目标） | 6 篇 |
| VQ 离散词表 | 单码本：[LaBraM](papers/fm/labram.md)、[NeuroLM](papers/fm/neurolm.md)、[TFM](papers/fm/tfm-tokenizer.md)；多码本 / RVQ / 双域：[CodeBrain](papers/fm/codebrain.md)、[NeuroRVQ](papers/fm/neurorvq.md)、[BrainRVQ](papers/fm/brainrvq.md)、[NeuroDETR](papers/fm/neurodetr.md) | 7 篇 |
| 注意力计算图改造 | 十字交叉（CBraMod）、隐空间压缩（LUNA）、线性化（[BIOT](papers/fm/biot.md)、TFM）、SSM+滑窗（CodeBrain）、因子化时空（[Not-All-EEG](papers/generative/not-all-eeg.md)） | 5 篇 |
| 生成目标做表征 | [EEGDM](papers/generative/eegdm.md)（encoder 不 detach 联合优化）、纯生成器 JET（[ICML 2026](papers/generative/jet.md)）、Not-All-EEG | 3 篇 |

三个观察（依据见对应笔记与综述）：

- **连续 patch + 掩码重构的差异化全靠附加件**：CBraMod 靠十字交叉注意力 + ACPE + 清洗语料（其附录 G 与表 13），LUNA 靠 query 压缩（8000 通道 FLOPs 为 BIOT 的 1/180，其表 4），REVE 靠 4D 坐标 PE + 块掩码 + 全局 token 瓶颈（其表 17–19 消融），EEGMoE 靠 SSMoE 域解耦（其消融）；附加件各自有效，但互比条件不同（[Kuruppu 综述](papers/reviews/kuruppu-critical-review.md) §5.1：评测任务异质，仅 4/10 可在公共任务排名）。
- **VQ 词表结构是 2025–2026 卷得最快的轴**：双码本、双域 RVQ、多尺度 RVQ、时频 motif 在一年内全部出现；[互怼链](comparison.md#critique-chain)中被指向最多的节点是 LaBraM（token 只当训练目标、展平注意力、通道平方复杂度、相位无贡献、单码本撞码等约 8 条批评边，均转写自各批评论文正文）。
- **「注意力形状匹配通道×时间网格」是被多论文独立验证的唯一设计原则**：CBraMod 消融 4:4 时空头最优、LUNA 通道维平方到线性、BrainGPT 用因果注意力管时序而把空间交给图网络（[comparison.md](comparison.md) §模型设计）。

## 3 痛点清单（按数据 / 方法 / 评测 / 落地）

### 数据

- **范式失衡**：癫痫域 27,062 h / 14,987 人，运动想象仅 152 h / 272 人，预训练被 TUEG 主导（[Yao 综述](papers/reviews/yao-eegfm-survey.md) §3.5 表 1）——直接后果是 FM 赢临床域、输 MI 域（Yao §6 自跑）；
- **预处理普遍极简**：无显式去伪迹、归一化语焉不详（[Kuruppu 综述](papers/reviews/kuruppu-critical-review.md) §5.1「Minimal data preprocessing」）；
- **上下文全部 ≤90 s**：没有任何 FM 能看 90 s 以上的长程模式（Kuruppu §5.2「Long temporal context」；最长者为 FoME 90 s，见其 §4.2）；
- 地理/性别偏置与隐私孤岛（[Chen 综述](papers/reviews/chen-representation-learning-review.md) §数据质量与开放科学；Kwon & Shin §6.1）。

### 方法

- **预训练目标与生理错配**：掩码 / 对比 / 自回归目标编码表面统计，不编码 PAC、跨通道相干、节律层级（[Kwon & Shin](papers/reviews/kwon-neural-fm-perspective.md) §4.2.1 与 §5.1）；
- 掩码切分破坏细粒时序结构（Yao §7.2；Chen 词元化节「切段边界破坏细粒度时序模式」）；
- VQ 难表达连续动态（Yao §7.2 对 LaBraM 的批评线）；
- **不变性对比学习在 EEG FM 中缺席**：Yao §4.2 明言增广不变型「尚未见于 EEG FM」，归因各任务增广需求不一致；站内仅 [BIOT](papers/fm/biot.md) 用结构型对比（SimCLR 式）。

### 评测

- **共享任务稀缺**：早期 10 个 FM 中仅 TUAB / TUEV 两个公共任务、4 个模型可比（Kuruppu §4.3 与其图 3）；
- **线性探针全线落后微调**：五个报告 LP 的模型无一例外（Kuruppu §5.2 与其图 4(a)）——注意这是该综述纳入范围内的观察，外推须注明任务与设定（站内已在 [Kuruppu 笔记](papers/reviews/kuruppu-critical-review.md) §7 收紧措辞）；
- **TUAB 已饱和**：传统方法 85–87%（Kuruppu §5.2 引 [152]）；
- 缺 FP/h 等临床实用指标与类不平衡反映（Kuruppu §5.2）。

### 落地

- 可解释性停留在 attention 可视化，无一被试模型通过神经科学有效性验证（Kwon §4.2.3；[Yao 综述](papers/reviews/yao-eegfm-survey.md) §7 把「幻觉」拆成两类）；
- 部署路径缺失：SaMD 监管、部署后漂移、模型卡均为提案状态（Kuruppu §6.3；Kwon §7）。

## 4 空白轴：≤1 篇或 0 篇

| 空白轴 | 现状 | 难点 | 证据 |
|---|---|---|---|
| 生理感知预训练目标 | **0 篇实现**（Kwon 提五项：PAC 预测、相干矩阵重建、相位锁定重排、跨模态预测、频率感知掩码） | 生理量噪声大、缺自监督真值 | [Kwon 综述](papers/reviews/kwon-neural-fm-perspective.md) §4 提案表 |
| 不变性对比 SSL | 0 篇（FM 范围内） | 各任务增广需求不一致 | [Yao 综述](papers/reviews/yao-eegfm-survey.md) §3 对比式一节 |
| >90 s 长上下文 | 0 篇 | 非平稳 + 显存双重制约 | [Kuruppu 综述](papers/reviews/kuruppu-critical-review.md) §5.2 |
| 事件 token / 变长集合输出 | 仅 [NeuroDETR](papers/fm/neurodetr.md) | 事件级标注稀缺、集合预测训练复杂 | 站内笔记 |
| Mamba 骨干 | 仅 [CodeBrain](papers/fm/codebrain.md)（混合 SSM）；FEMBA / MENTALITY 为站外先行 | 刚有人踏入，证据少 | [Chen 综述](papers/reviews/chen-representation-learning-review.md) 骨干分类 |
| 借 LLM | 仅 [NeuroLM](papers/fm/neurolm.md)（GPT-2） | EEG-文本无成对数据，只能退到对抗式空间对齐 | 站内笔记 |

## 5 scaling：四组证据的口径对照

领域最大的悬而未决问题是「堆数据有没有用」。站内可核查的四组证据，口径各不相同，不能合并成一条曲线：

| 证据 | 改动变量 | 条件 | 结果 | 出处 |
|---|---|---|---|---|
| LaBraM 数据消融 | 预训练 1–2500 h × 三档模型 | TUAB / TUEV | ~1000 h 后趋平（作者曲线） | [Yao 综述](papers/reviews/yao-eegfm-survey.md) §5；Kuruppu §5.2 |
| EEGPT 受控对照 | 预训练数据 12.5%–100% | BCIC-2A/2B | 见其附录 A.5 | [选读页 §四](blog-2023-2026.md#_4) |
| EEGArena 固定架构 | REVE-base 架构不变，语料 600h→30k h | 全量微调 | 被试内 +6.69pp | [EEGArena](papers/survey/eegarena.md) §2.6、§3.4 |
| Kuruppu 跨研究对照 | 4.5k–878k channel-hours | TUAB/TUEV | 无正相关 | [Kuruppu 综述](papers/reviews/kuruppu-critical-review.md) §5.2 |

读法（站内推断，非原文结论）：数据缩放效应**是否存在取决于任务与协议**——EEGArena 的受控对照说明增益存在但需固定架构，Kuruppu 的跨研究对照说明「报得多」不等于「效果好」；两者不矛盾，因为前者控制了架构变量而后者没有。这正是 §3 评测痛点（协议不可比）的直接代价。

## 6 正在被修正的三个叙事（站内证据）

1. **「FM 普遍优于简单基线」**：EEGArena 显示参数量不预测性能（其 §3），Yao §6 自跑显示 MI 域 FM 全线输 EEGNet——但 EEGArena 同时显示「FM 大多领先」且固定架构的预训练数据缩放有增益（受控对照见[实验证据](evidence.md)）。合成的结论是：**FM 的优势有条件（任务域、协议、数据规模），不是普适的**。
2. **「线性探针差 = 实现问题」**：Kuruppu 在其纳入范围内报告 LP 落后 FT 跨五个模型出现（其图 4(a)；纳入范围与任务设定见[其笔记](papers/reviews/kuruppu-critical-review.md)）——凡做「冻结可用」主张的工作（[EEGPT](papers/fm/eegpt.md) 的对齐目标、[REVE](papers/fm/reve.md) 的全局 token 瓶颈）都是在对着这个观察设计，其普遍性尚待更大范围验证。
3. **「架构 vs 预训练」二选一**：REVE 的预训练价值消融（其表 3：PhysioNet-MI 上无预训练 REVE 0.5409 < CBraMod 0.6196；有预训练 REVE 0.6480 > CBraMod 0.6417）把两种来源的贡献同框量化——架构先验与预训练数据各有其适用面，站内判断详见 [REVE 笔记的个人思考](papers/fm/reve.md)。

## 7 站外动态（检索所得，站内未核对原文，引用前须核实）

以下条目来自 2026 年网络检索，**未入站内精读库**，列出仅为方向参考：

- 2026 新模型：BrainCodes（量化神经 tokenizer，1.9M）、ERP-FM（通用 ERP 基础模型）、BioFoundation（拓扑无关）、iBrain / DIVER-1（颅内scaling研究）、PHASE（生理引导分层目标）；
- 新评测：EEG-FM-Compass 登 NSR（站内已引其结论，见 [CBraMod 笔记](papers/fm/cbramod.md)）；「负对照协议」与受控评测类工作要求新 FM 论文必须报 random-init 与 band-power 基线；
- 被质疑的方向：dataset identity 泄漏（模型编码电极配置/数据集身份而非神经信号）、纯 EEG-text 对齐收益最低；
- 落地信号：FDA 2026-01 批准首个 foundation-model 平台（Aidoc）。

## 8 对研究选型的含义（站内推断）

1. **纯做「更好的坐标 PE」空间很小**——REVE 已占坐标生成位。空白轴①的组合方向（坐标 PE × 生理感知目标）同时吃到 §4 两个空白，且与蒙太奇多样性实验互证；
2. **VQ 词表结构轴已高度拥挤**（§2），新词表工作需要回答「token 用途」而非「token 结构」的差异化——TFM（token 作输入）与 NeuroDETR（token 作事件记忆）是用途差异化的两个样本；
3. **新评测环境下的必答题**：random-init 基线、OOD 评测、LP/FT 并报——Kuruppu 的批判清单（§6 基准与工具）与 EEGArena 的协议正在变成事实标准；
4. **写作引用纪律**：四篇综述互有转述失真（如 Kwon 对 CBraMod 的「对比目标」误读，见[其勘误节](papers/reviews/kwon-neural-fm-perspective.md)），模型设计事实应回原文核对，综述仅作地图使用。

---

**相关阅读**：四篇综述精读——[Yao（技术分类与复跑比较）](papers/reviews/yao-eegfm-survey.md) · [Chen（组件拆解与迁移学习）](papers/reviews/chen-representation-learning-review.md) · [Kuruppu（评测批判与代表性）](papers/reviews/kuruppu-critical-review.md) · [Kwon（设计原则主张）](papers/reviews/kwon-neural-fm-perspective.md) ｜ [实验证据](evidence.md) ｜ [EEGArena](papers/survey/eegarena.md) ｜ [十四篇方法对比](comparison.md) ｜ [EEG 预训练数据全景](topics/data-landscape.md) ｜ [首页](index.md)
