---
title: 首页
---

# ![CyLin-CSU](https://github.com/CyLin-CSU.png){ .h1-avatar } EEG 论文阅读笔记

> CyLin-CSU · 精读 **31** 篇（2023–2026）· 按模型、任务和数据集查阅 EEG 论文笔记

**[浏览论文](#papers)** ｜ **[方法对比](comparison.md)** ｜ **[主题专题](#topics)** ｜ **[从哪篇综述读起](blog-2023-2026.md#综述速览)** ｜ **[论文库筛选](library.md)** ｜ **[模型并排对比](models.md)** ｜ **[实验证据](evidence.md)**

按任务直达：**看预训练目标** → [预训练范式对比](topics/pretraining.md) ｜ **找数据集下载与用途** → [数据集索引](datasets.md) ｜ **读预训练语料与报告规模** → [数据全景专题](topics/data-landscape.md) ｜ **读领域全景与争议** → [EEG 基础模型全景](landscape-2026.md) ｜ **读领域综述** → [综述与观点（4 篇）](#papers-reviews) ｜ **比通道适配方案** → [通道适配与多任务](topics/multi-task.md)

## 论文库 {: #papers }

完整 31 篇可筛选目录见 [论文库](library.md)（类型 / 分组 / 年份 / 代码与 DOI 可用性筛选，链接可复现筛选状态）；按字段并排比较见 [模型对比](models.md)。以下为各组入口与近期收录。

### EEG 基础模型（15 篇） {: #papers-fm }

- [REVE](papers/fm/reve.md) · NeurIPS 2025 —— 4D 傅里叶位置编码适配任意电极布局，61,415h 预训练（[模型卡](models.md)）
- [Uni-NTFM](papers/fm/uni-ntfm.md) · ICLR 2026 —— 时域/频带功率双向交叉注意力 + 拓扑嵌入 + MoE
- [CodeBrain](papers/fm/codebrain.md) · ICLR 2026 —— 时/频双码本解耦 + 多尺度 SSM 骨干

全部 15 篇：[论文库 · EEG 基础模型](library.md?group=fm)；按维度横读见下方[主题专题](#topics)。

### 生成式模型（3 篇） {: #papers-generative }

- [JET](papers/generative/jet.md) · ICML 2026 —— 条件流匹配 + 生理结构约束，直接生成原始 EEG
- [EEGDM](papers/generative/eegdm.md) · arXiv 2026 —— 潜扩散生成目标做表征学习
- [Not-All-EEG](papers/generative/not-all-eeg.md) · arXiv 2026 —— 按位置难度调整流匹配时间调度

### 综述与观点（4 篇） {: #papers-reviews }

- [EEG FM 综述 (Yao)](papers/reviews/yao-eegfm-survey.md) · JNE 2025 —— 预训练三路线横评 + 自跑 10 模型 × 6 数据集
- [表示学习与 FM 综述 (Chen)](papers/reviews/chen-representation-learning-review.md) · IEEE SPM 2025 —— 18 模型组件拆解表 + 迁移学习地图
- [EEG FM 批判综述 (Kuruppu)](papers/reviews/kuruppu-critical-review.md) · JNE 2026 —— 评测异质、scaling 证据弱、LP 落后 FT 的证据清单
- [神经信号 FM 观点 (Kwon)](papers/reviews/kwon-neural-fm-perspective.md) · EJN 2026 —— 生理目标/结构先验/可解释三原则

### 相关研究（9 篇） {: #papers-survey }

- [EEGArena](papers/survey/eegarena.md) · arXiv 2026 —— 30 FM × 25 基线 × 57 任务的统一评测
- [LTFT](papers/survey/learnable-tf.md) · TETCI 2026 —— 时频变换窗口设为可学习参数的信号前端
- [NPI](papers/survey/surrogate-brain.md) · Nature Methods 2025 —— 代理脑虚拟扰动估计脑区间有效连接

全部 9 篇：[论文库 · 相关研究](library.md?group=survey)

## 主题专题与架构基础 {: #topics }

| 页面 | 说明 |
|---|---|
| [EEG Tokenization 演进](topics/tokenization.md) | 比较连续片段、离散码字及其训练用途。 |
| [预训练范式对比](topics/pretraining.md) | 对比 / 掩码 / 自回归 / 生成四路线与掩码目标进化 |
| [通道适配与多任务学习](topics/multi-task.md) | 通道表示、空间整合与任务共享方式 |
| [EEG 预训练数据全景](topics/data-landscape.md) | 语料构成、域偏斜与规模瓶颈 |
| [基座来源分析](topics/base-model.md) | 从零训练 vs 加载现成基座 |
| [语音模型专题](topics/speech-models.md) | 语音解码轴线按 tokenization / pretraining / 下游任务横读 |
| [LoRA · 低秩适配](basics/lora.md) | 参数高效微调事实标准 |
| [Attention 替代方案](basics/attention-alternatives.md) | 线性注意力 → Mamba-2 → 混合 → DSA |
| [生成模型脉络](basics/generative-lineage.md) | ELBO / 去噪 / 速度场三代绕法 |
| [图神经网络](basics/gnn.md) | 消息传递与 GAT，BrainGPT TEG 的机制基础 |

另有：[十四篇方法对比](comparison.md)（九维度横向对照）· [数据集索引](datasets.md)（14 × 36 使用矩阵）· [EEG 基础模型选读](blog-2023-2026.md)（对外选读版，含「从哪篇综述读起」速览）· [EEG 基础模型全景](landscape-2026.md)（研究重点 / 痛点 / 空白轴，全论断带出处）· [参考文献索引](references.md)。

## 最近更新 {: #updates }

最近提交：<!-- LAST_UPDATE -->（北京时间）· <!-- ACTIVITY_BADGE -->

<div class="ac-slot"><!-- ACTIVITY_CALENDAR --></div>

<ul class="timeline" id="home-timeline" markdown>

- **2026-11-19** · 新增领域全景页（landscape-2026）：研究重点、四类痛点、创新拥挤度、六条空白轴与 scaling 证据对照——全部论断标注站内笔记或综述节号出处

- **2026-11-18** · 综述四篇齐发：[Yao（JNE 2025）](papers/reviews/yao-eegfm-survey.md) 自跑 10 模型 × 6 数据集，FM 赢临床域、输 MI，根子在被癫痫数据主导的预训练域 · [Chen（IEEE SPM 2025）](papers/reviews/chen-representation-learning-review.md) 18 模型按词元化/嵌入/位置编码/骨干/损失逐项拆表 · [Kuruppu（JNE 2026）](papers/reviews/kuruppu-critical-review.md) 三支柱批判：评测异质、scaling 证据弱、LP 落后 FT · [Kwon & Shin（EJN 2026）](papers/reviews/kwon-neural-fm-perspective.md) 生理先验/结构感知/可解释三原则，判现存 FM 为第一代（其 CBraMod「对比目标」转述与原文不符，站内已标注）

- **2026-11-06** · 新增 [Uni-NTFM](papers/fm/uni-ntfm.md) 精读，拆解时域与频域双向交叉注意力、分层拓扑嵌入和双域掩码重建。

- **2026-11-05** · 新增精读 REVE（NeurIPS 2025）：电极坐标与时间构建 4D 傅里叶位置编码，支持不同电极布局与序列长度；92 数据集 61,415h 预训练语料（论文称非侵入最大）——10 任务微调平均较 CBraMod +2.5%（其表 2），linear probing 均值 REVE-L 0.654 / CBraMod 0.501（其表 4，无池化列），对比集扩至十四篇

- **2026-11-04** · tokenization 线五篇齐发：NeuroRVQ（多尺度 RVQ，EEG 重构 MSE 较 LaBraM 降 67 倍）· BrainRVQ（时/频双域 RVQ）· CodeBrain（时/频双码本解耦）· NeuroDETR（VQ 事件记忆 + DETR 式事件检测，8 数据集 F1 全第一）· DELTA（RVQ + 掩码语言扩散 EEG-to-Text）——tokenization 演进页此前列出的缺口均有对应工作

- **2026-11-04** · 新增精读 GUIDED（ATM · arXiv 2024）：EEG 映进 CLIP 空间 + 冻结 SDXL 两阶段引导扩散重建所见图像——站内「视觉重建」轴线第一篇，EEG 与 MEG/fMRI 首次同桌比较

- **2026-11-04** · 新增精读 CrossPT-EEG（arXiv 2024 · 清华）：16 人 × 22 session 视觉解码泛化基准，比较被试内、跨时间与跨被试三种设置——two-way ID 被试内均值 0.95、跨时间 0.51、跨被试 0.49（均为对应设定均值）

- **2026-11-04** · 新增 EEGArena 精读，记录 57 项任务的统一评测与预训练数据规模实验（数值见[实验证据](evidence.md)）

- **2026-11-03** · 新增语音模型专题（与主题专题并列）：语音解码轴线按 Tokenization / Pretraining / 下游任务三段横读——脑端不切段、语音端选空间、监督对齐范式与检索/回归/生成三协议

- **2026-11-03** · 重整五个主题专题，合并通道适配与多任务；补入 NeuroRVQ、BrainRVQ、CodeBrain、NeuroDETR，更新写作说明。单篇笔记仍为 17 篇。

- **2026-11-02** · 新增精读 Défossez 语音解码（NMI 2023）：卷积脑模块对比对齐 wav2vec 2.0——3 秒 MEG 千余候选 zero-shot 检索所听语句，站内「语音解码」轴线的源头文献

- **2026-11-02** · 新增精读 SSM2Mel（arXiv 2025）：Mamba+MHSA 交替骨干重建连续语音 mel 谱——语音解码轴线从检索走向回归

- **2026-11-02** · 新增精读 LTFT（IEEE TETCI 2026）：逐频率复值窗口随梯度更新——频域学习从损失端（Not-All-EEG 加权）搬进变换核本身

- **2026-11-02** · 新增轴外精读 NPI（Nature Methods 2025）：把训好的网络当可干预的脑，虚拟扰动读出方向性全脑有效连接——「模型作科学工具」与站内「模型作解码器」对望

- **2026-10-28** · 新增精读 Not-All-EEG（arXiv 2026）：位置自适应时间调度——EMA 误差图把流匹配的全局 t 展开成通道×位置时间图，TS-FID 对 JET 再降 40–62%，生成轴线第三篇

- **2026-10-27** · 对比体系重构：comparison 收敛为枢纽页（速览 + 九维导读 + 战绩/互怼链），维度详解下放六大专题页，各专题覆盖扩至十二篇

- **2026-10-17** · 模型架构基础新增：图神经网络——消息传递 / 谱卷积 / GAT / 表达力边界，BrainGPT TEG 的机制基础

- **2026-10-17** · 新增精读 EEGDM（arXiv 2026）：潜扩散生成目标替代掩码重构——encoder 表示作扩散条件联合优化，TUEV 类不均衡指标全场最佳

- **2026-09-28** · 新增精读 CBraMod（ICLR 2025）：十字交叉注意力 + 非对称条件位置编码——EEG-FM-Compass 统一 benchmark 综合第一

- **2026-09-26** · 模型架构基础新增：生成模型三代脉络（VAE → DDPM → Flow Matching），一条主线串起 ELBO、得分匹配与速度场回归

- **2026-09-24** · 新增双篇精读：EEGMoE（域解耦 MoE）× LUNA（拓扑统一）——通道异构问题的两条相反路线；专题页新增第五/六种解法

- **2026-09-23** · 新增精读 JET（ICML 2026）：条件流匹配生成原始 EEG + 三条生理结构约束——站内首篇「生成」轴线论文

- **2026-09-22** · 模型架构基础新增：Attention 替代方案（线性注意力 → Mamba-2 → Gated DeltaNet → 混合 → DSA），整理自 Stanford CS336 Lec 4

- **2026-09-21** · 新增跨领域精读：RF-GPT——射频时频图 + 多模态 LLM（RFLM 概念首作）

- **2026-09-21** · 新增分类「模型架构基础」：首篇 LoRA 低秩适配精读（原论文 + 变体族谱 + EEG 语境用法）

- **2026-09-20** · 全站内容审查：2 个审查代理核查 21 处问题并全部修复（含数据集矩阵严重错误）

- **2026-09-19** · 新增专题：基座来源分析（从零训练 vs 现成 Base Model）

- **2026-09-19** · 数据集索引新增 数据集×论文 使用矩阵热力图

- **2026-09-18** · 组件大升级：Mermaid 流程图/内容标签页/脚注/术语提示/图片放大/阅读进度条/对比图表

- **2026-09-18** · 新增自问自答区、参考文献索引、数据集索引；移除活跃热力图；修复数学公式渲染
- **2026-09-18** · 站点 v1.2：主页改版，新增更新时间线与活跃状态
- **2026-09-18** · 新增 3 个主题专题：Tokenization 演进 / 预训练范式 / 通道异构解法
- **2026-09-18** · 完成 6 篇精读：BIOT · LaBraM · EEGPT · BrainGPT · NeuroLM · TFM-Tokenizer

</ul>

## 阅读统计 {: #stats }

| 统计项 | 数值 |
|---|---|
| 精读论文 | 31 篇（EEG 基础模型 15 + 生成式模型 3 + 相关研究 9 + 综述与观点 4） |
| 发表跨度 | 2023 – 2026 |
| 涉及会议/期刊 | NeurIPS ×3 + 1 WS · ICLR ×6 · ICML ×1 · TNNLS ×1 · NMI ×1 · Nature Methods ×1 · TETCI ×1 · JNE ×2 · IEEE SPM ×1 · EJN ×1 · arXiv ×11（另基础页 ICLR 2022 / CS336） |


## 留言板 {: #comments }

欢迎留言交流——提问、纠错、推荐新论文都可以。

<div id="giscus-container" data-loading="lazy"></div>
