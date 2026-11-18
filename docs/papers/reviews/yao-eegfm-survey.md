---
date: 2026-11-18
title: "Foundation models for EEG decoding: current progress and prospective research"
authors: [Yuxuan Yao, Hongbo Wang, Li Chen, Yiheng Peng, Jingjing Luo]
venue: "J. Neural Eng. 2025"
year: 2025
tags: [综述, EEG基础模型, 掩码重构, 自回归, 预训练策略, 范式失衡]
status: "精读"
rating: 4
doi: "10.1088/1741-2552/ae17e9"
arxiv: ""
code: ""
one-liner: "PRISMA 综述 + 自跑 10 模型 × 6 数据集：掩码重建是主流预训练路线，FM 赢临床域、输 MI 域，根子在预训练数据被癫痫范式主导"
---

# Foundation models for EEG decoding: current progress and prospective research

> **J. Neural Eng. 22, 061002（2025）· Topical Review**

**作者**：Yuxuan Yao、Hongbo Wang、Li Chen、Yiheng Peng（复旦工研院 AIR）、Jingjing Luo（通讯，中南大学）

## 1 问题定位

监督式 EEG 模型任务特定、数据依赖重。本文用 PRISMA 流程筛 EEG-only、含预训练、有泛化评测的近五年工作，按「任务与数据集 / 预训练策略 / 架构」三条线梳理，并补一场统一协议的性能对比。特色是**自己跑了对比实验**：10 个模型 × 6 个数据集，原论文报告值（彩色）与自跑补齐值（黑色）分开标注。

## 2 任务与数据集：范式失衡

五个下游任务域（癫痫 / MI / 情绪 / 睡眠 / 其他）的常用数据集汇总成表，按总时长一排就看出口径差距：

| 任务域 | 被试数 | 总时长 | 典型数据集 |
|---|---|---|---|
| 癫痫（TUEG 系） | 14 987 | 27 062 h | TUEG / TUAB / TUEV / TUSZ / TUEP / TUAR / TUSL |
| 睡眠分期 | 347 | 6 035 h | SleepEDFx / HMC / ISRUC |
| 情绪识别 | 275 | 193 h | SEED 系 / FACED / DEAP / DREAMER / MAHNOB-HCI |
| 运动想象 | 272 | 152 h | BCIC IV-2a/2b / HGD / PhysioNet-MI / SHU-MI / OpenBMI |

§3.5 是全文最有价值的论点：现有 FM 预训练基本被 TUEG 一类临床癫痫数据主导，与 MI / 情绪等下游范式差异大，形成域差；文中引的一项研究显示部分预训练模型从头训练还不如任务专用模型。多范式联合预训练是数据侧的待解问题。另有一个次要观察：睡眠数据时长可观但通道少（2–6 导），因此很少被用作 FM 预训练主料。

## 3 预训练策略分类

### 3.1 分类总表

| 大类 | 子类 | 代表 | 一句话机制 |
|---|---|---|---|
| 生成式 | 自编码器重构 | EEGFormer（+VQ）、DFformer | encoder–decoder 直接重构输入；DFformer 用类 token 生成基矩阵重构 |
| 生成式 | 掩码重构·通道级 | TSP | 直接删通道，重空间轻局部时间 |
| 生成式 | 掩码重构·patch 级（随机） | BENDR、LaBraM、MAEEG | 随机掩时间步/段；简单高效但可能退化成插值 |
| 生成式 | 掩码重构·patch 级（块状） | MAE-EEG-Transformer | 遮整段时间段，保留上下文 |
| 生成式 | 掩码重构·定制 | EEG2Rep（SSP 策略） | 动态保留语义关键段，掩码两侧语义量最大化 |
| 生成式 | 重建空间·信号级（MAE 式） | 多数 FM | 重构原始波形，最常用 |
| 生成式 | 重建空间·embedding 级（BERT 式） | CBraMod、EEG2Rep、TSP | 重构被掩 embedding，参数省但丢信号保真 |
| 生成式 | 重建空间·离散级（BEiT 式） | LaBraM | 先 VQ 量化再预测码字，紧凑可解释 |
| 生成式 | 自回归 | BrainGPT（站内口径，原文 EEGPT(2)） | 因果单向，凭过去预测未来信号 |
| 生成式 | 多域·空间 | MMM、GMAEEG | 拓扑/图结构建模，多维 PE 或自适应邻接矩阵 |
| 生成式 | 多域·频率 | Neuro-BERT、LaBraM | 傅里叶幅相预测 / VQ 神经频谱预测 |
| 对比式 | 增广不变型 | **EEG FM 中尚未出现** | 同一样本两增广互为正对；归因于各任务增广需求不一致 |
| 对比式 | 结构型（CPC） | BENDR、TSP | 预测未来表示并与负样本对比，防任务退化成插值 |

### 3.2 三条作者口径的观察

- **掩码率 ~50%**，低于图像的 75–90%——解释是 EEG 语义冗余低于图像，激进掩码会破坏基本时序模式；
- **AR 与时序结构天然契合**但受非平稳、低 SNR 拖累，所以双向掩码（MAE 式）反而更常用；
- **同架构对照**（BrainGPT，站内口径）：睡眠分期 AR 77.9% > MAE 74.8%，由此推测 **AR 适合时间连续任务、掩码适合信号突变任务（如棘波癫痫）**——尚属初步结论，文中明言预训练策略研究仍处早期、无共识。

## 4 架构组件

| 组件 | 主要选项 | 代表与取舍 |
|---|---|---|
| 切段 | instance-wise（整窗按时序切，含全部通道） | 卷积做空间建模，适合单数据集（BENDR、EEG2Rep、Neuro-BERT） |
| 切段 | channel-wise（逐通道切 patch） | 天然适配变导联配置，跨数据集预训练的通行做法（LaBraM、CBraMod 一系） |
| patch 嵌入 | 1D 卷积提时序特征（主流） | wave2vec 2.0 式：conv + norm + activation |
| patch 嵌入 | 频域能量向量 | Fourier 变换逐 patch 提能量再过全连接（部分 FM） |
| patch 嵌入 | 空间卷积 | 形状绑定导联数，多数据集预训练需改结构 |
| 位置编码 | 可学习静态（主流） | 正弦余弦因采样率绑定而少见 |
| 位置编码 | 动态·RoPE | EEGPT（站内口径 Wang et al.）——位置相关旋转捕捉相对关系 |
| 位置编码 | 动态·条件位置编码 | CBraMod 非对称双轴：短程管时间、长程管空间 |
| 位置编码 | 空间·通道嵌入 | 每导联一个可学习向量（多 FM 采用） |
| 位置编码 | 空间·物理坐标 | 电极 2D/3D 坐标 + 拓扑距离（TSP、MMM） |
| 骨干 | encoder-only Transformer | 压倒性多数，~12 层 + 线性/MLP 头 |
| 骨干 | decoder-only（自回归） | Neuro-GPT、BrainGPT（站内口径） |
| 骨干 | ViT 直接搬用 | Neuro-BERT、EEGPT（站内口径） |
| 骨干 | Mamba | 仅 FEMBA（双向 Mamba encoder） |
| 注意力 | 双向 MHSA（重构系） | 默认配置 |
| 注意力 | 因果 MHSA（自回归系） | 因果掩码保证只见过去 |
| 注意力 | 时空分离注意力 | 时序/空间各生成独立 QKV（EEGFormer、FoME） |
| 注意力 | 十字交叉 | CBraMod：头分组分别做空间/时间注意力 |
| 注意力 | 交叉注意力 | EEG2Rep 重构时增强上下文与被掩 token 的关联 |

§5.6 的批评：当前 FM 的注意力机制创新有限，交叉注意力等已在 EEG 预训练框架中证明有效的设计尚未充分进入 FM。

## 5 技术设计总表（原表 2 复现）

原文表 2 逐项汇总 16 个 FM/预训练框架的设计字段，站内按原文转录（「—」为原文未报）：

| 方法 | 年份 | 预训练技术 | 切段 | patch 嵌入 | 位置编码 | 骨干 | 参数量 |
|---|---|---|---|---|---|---|---|
| BENDR | 2021 | 掩码建模 + CPC | instance-wise | Conv·时域 | 条件 PE·时间 | Transformer encoder | 1B |
| MAEEG | 2022 | 掩码重构 | instance-wise | conv encoder·时域 | 条件 PE·时间 | Transformer encoder | — |
| BIOT | 2023 | channel-token 双掩码重构 | channel-wise | FFT+Linear·频域 | 相对 PE·时间 | 线性 Transformer | 3.3M |
| MMM | 2023 | 全局+区域掩码重构 | channel-wise | DE 特征 | 多维 PE·空间 | Transformer encoder | — |
| LaBraM | 2024 | VQ-VAE 掩码码字预测 | channel-wise | Conv·时域 | 绝对 PE·时空 | Transformer encoder | 5.8M / 46M / 396M |
| CBraMod | 2024 | 掩码重构 | channel-wise | Conv·时域 + FFT·频域 | 非对称条件 PE·时空 | Criss-Cross Transformer | 4.0M |
| FoME | 2024 | 掩码重构 | channel-wise | Linear·时域 + FT·频域 | 绝对 PE·时间 | 时序&空间 Transformer | 476.3M / 744.8M |
| Neuro-BERT | 2024 | 傅里叶反演掩码重构 | instance-wise | Conv·时域 | 相对 PE·时间 | ViT | 2.1M |
| EEGPT（站内口径） | 2024 | 掩码重构 | channel-wise | Linear·时域 + 通道嵌入·空间 | RoPE·时间 | ViT | 25M |
| MAE-EEG-Transformer | 2024 | 掩码重构 | instance-wise | Conv·时域&空间 | 绝对 PE·时间 | Transformer encoder | 0.19M |
| GMAEEG | 2024 | 图掩码重构 | — | — | — | CNN + GCN | — |
| TSP | 2024 | 掩码重构 + CPC 时间预测 | instance-wise | STFT·频域 | 绝对 PE·空间 | 动态 CNN / Transformer | — |
| DFformer | 2024 | 信号重构 | instance-wise | Conv·时域 | 绝对 PE·时空 | Domain-free Transformer | — |
| EEGFormer | 2024 | VQ-VAE 信号重构 | channel-wise | Linear·时域 | 绝对 PE·时间 | Transformer | — |
| Neuro-GPT | 2024 | 因果掩码预测 | instance-wise | conv+自注意力·时空 | — | Decoder-only Transformer | 56.6M |
| BrainGPT（站内口径，原文 EEGPT(2)） | 2024 | 自回归重构 | channel-wise | Linear·时域 + 通道嵌入·空间 | — | Causal Transformer | 1.46M–1.09B |
| FEMBA | 2025 | 掩码重构 | channel-wise | Conv·时域 | 绝对 PE·时间 | 双向 Mamba | 7.8M–386M |

预训练/下游数据集按原文表 2 附注：BENDR / Neuro-GPT / CBraMod / EEGFormer / FEMBA 以 TUEG 系为主；LaBraM 用 TUH + SEED 系等约 20 个数据集；BIOT 用 PREST + SHHS；EEGPT（站内口径）用 PhysioMI/HGD/TSU/SEED/M3CV；BrainGPT（站内口径）用 FACED/SEED 系/THINGS-EEG。

## 6 自跑对比：临床域赢、MI 域输

协议：6 数据集（TUAB / TUEV / BCIC IV-2a·2b / SleepEDFx / SEED-V），统一预训练权重 + 全参微调，50 epoch AdamW（lr 5e-4、wd 5e-2），不支持变通道的模型前置一个空间滤波卷积；MI 用 LOSO；每格 5 次重复报均值。基线两组：从头训练的 EEGNet / EEGConformer / CNN-Transformer，与预训练 FM（LaBraM / BENDR / Neuro-GPT / EEGPT / CBraMod / BIOT，BIOT 另含 ECG 数据）。

正文口径的关键数字（原表 3 存在黑/彩混排，站内只转录正文明确给出的数值，其余以「—」留白）：

| 模型 | 参数量 | TUAB | TUEV | BCIC IV-2a | BCIC IV-2b | SleepEDFx | SEED-V |
|---|---|---|---|---|---|---|---|
| EEGNet | 0.003M | 0.7642 | 0.3876 | **0.6879** | **0.7321** | — | — |
| EEGConformer | 0.55M | 0.7758 | 0.4074 | — | — | — | — |
| CNN-Transformer | 3.2M | 0.7777 | 0.4087 | — | — | — | — |
| BIOT | 3.2M | 0.7959 | 0.5281 | — | — | — | — |
| BENDR | 4.0M | 0.7323 | 0.4619 | 0.4899 | 0.7067 | — | — |
| LaBraM-Base | 5.8M | 0.8140 | 0.6409 | — | — | 0.6771 | 0.4095 |
| Neuro-GPT | 56.6M | **0.7889** | **0.5501** | — | — | — | — |
| EEGPT（站内口径） | 25.3M | 0.7983 | 0.6232 | 0.5846 | 0.7212 | — | — |
| CBraMod | 4.0M | 0.8289 | 0.6671 | — | — | 0.6221 | 0.4091 |

四个读数：

- **临床域 FM 大胜**：TUAB/TUEV 领先者均为 FM（自跑口径 Neuro-GPT 领先、原报告口径 CBraMod 更高），作者归因于预训练域与癫痫数据同源；
- **MI 全线失守**：EEGNet 两个数据集最高，BENDR 2a 仅 0.4899——低 SNR + 范式域差双重归因；
- **中间地带**：LaBraM-Base / CBraMod 在 SleepEDFx、SEED-V 尚有竞争力，说明跨范式泛化并非不可能；
- **成本注脚**：EEGNet 0.003M vs Neuro-GPT 56.6M——增益换参数，资源受限场景要另算账。

另有两处跨报告数值不一致被点名：EEGNet 在 2a（0.4482–0.5130）、EEGConformer 在 SEED-V（0.2650–0.3537）、LaBraM-Base 在 SEED-V（0.2640–0.4095）——来源是预处理、超参或训练协议差异。这本身就是「评测碎片化」的直接证据。

## 7 可解释性与可信性盘点

- **可解释性**：Grad-CAM（CBraMod 的 MI 激活落在 C3/C4 运动皮层）、时序显著性图（EEGFormer 的癫痫段落落在 Fz/Pz/T3/T6）、注意力拓扑图（MAE-EEG-Transformer）；
- **可信性**：EEG2Rep 在高斯噪声 / DC 偏移 / 幅值缩放扰动下最多降 3.21%；t-SNE/UMAP 显示预训练表示已带类别结构，微调后更分明；
- **幻觉**分两类：关注无关区域仍给出置信预测（要靠可解释性防）、不看任务特征碰对答案（要靠表示空间检查防）。

## 8 展望四条

信号导向的 pretext 任务（现有任务把 EEG 当图像/文本段处理，忽视突变与时序依赖）；EEG 定制对比学习框架；注意力机制优化（低 SNR、被试变异量身定制）；多模态 SSL（卡在对齐数据稀缺）。

## 9 站内视角

- 本文与 [EEGArena](../survey/eegarena.md) 互补：一个纵评预训练策略（固定协议自跑），一个横评 FM 对监督基线（各模型专属预处理）。MI 结论不一致（EEGArena 称 FM 大多领先，本文称 FM 输 EEGNet），协议与任务池不同，站内不做合并推断。
- 命名陷阱：文中 EEGPT(1) = 站内 [EEGPT](../fm/eegpt.md)（Wang et al., NeurIPS 2024），EEGPT(2) = 站内 [BrainGPT](../fm/braingpt.md)（Yue et al.）。引用两篇时注意消歧。
- §3.5 的域差论证是数据侧动机的直接引文，[数据全景专题](../../topics/data-landscape.md) 可对接。
- §5 技术设计总表与 [Chen 综述的拆解表](chen-representation-learning-review.md) 互为印证——两表字段口径不同（本表含注意力机制与数据集，Chen 表含损失与开源信息），合读可互补。

---

**相关阅读**

:material-format-list-bulleted: [EEGArena（互为镜像的评测视角）](../survey/eegarena.md) ｜ :material-shield-search: [CBraMod（本榜临床域自跑第一梯队）](../fm/cbramod.md) ｜ :material-electric-bolt: [BrainGPT（文中 EEGPT(2)，AR vs MAE 同架构对照）](../fm/braingpt.md) ｜ :material-cog: [预训练范式专题（目标/掩码/范式同一口径）](../../topics/pretraining.md) ｜ :material-script-text: [站内 EEG 基础模型选读（可对照其取舍）](../../blog-2023-2026.md) ｜ :material-clipboard-check: [Chen 综述（拆解表口径互补）](chen-representation-learning-review.md) ｜ :material-home: [首页](../../index.md)
