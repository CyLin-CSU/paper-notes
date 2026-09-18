# 六篇方法对比

7. 六篇方法对比

#### 7.1 总览表

| 维度 | BIOT | LaBraM | EEGPT | BrainGPT | NeuroLM | TFM-Tokenizer |
|---|---|---|---|---|---|---|
| **发表** | NeurIPS 2023 | ICLR 2024 | NeurIPS 2024 | arXiv 2024 | ICLR 2025 | ICLR 2026 |
| **定位** | 轻量跨格式编码器 | 大规模 EEG 基础模型 | 通用特征提取器（小模型） | 自回归 generalist | 接 LLM 的多任务基础模型 | 可插拔 tokenization 组件 |
| **token 形式** | 连续向量（规则切段） | 离散码（**仅作预训练目标**） | 连续 patch embedding | 连续 1s 片段（无离散化） | 离散码（**并入 LLM 词表作输入**） | 离散码（**作下游输入**） |
| **词表** | 无 | 8192×64（标签空间） | 无 | 无（电极词表另算） | 8192 并入 GPT-2 词表 | 8192（输入嵌入空间） |
| **预训练目标** | BYOL 式对比学习（丢通道/丢token→扰动→对比） | 掩码码字预测（BEiT 式）+ 对称掩码 | 表示对齐（JEPA 式）+ 掩码重构（MAE 式）双自监督 | 因果下一 token 预测（自回归回归原始值，MSE） | 多通道自回归（阶梯掩码预测离散码）+ GRL 对抗空间对齐 | 频带+时间+对称掩码的频谱图重构（训 tokenizer）→ masked token prediction（训下游） |
| **频域角色** | FFT 能量→FCN 作 segment embedding 特征 | DFT 幅值+相位作为 tokenizer 重构目标 | 无显式频域 | 无显式频域 | 时域信号 + DFT 幅值双 decoder 重构 | **双路径显式建模**（频率 Transformer + 门控聚合）+ 频带掩码 |
| **空间建模** | channel embedding + 正弦位置编码 | 可学习空间 embedding（10-20 系统） | Codex book 通道表（名字→向量映射） | 电极条件 prefix token + 下游 TEG 图注意力 | 空间 embedding | 单通道训练，多通道拼接 + 通道 embedding |
| **位置编码** | 有（正弦相对） | 有（可学习时+空） | RoPE（predictor 内） | GPT 式 | 复用 LLM 时间 emb + 新空间 emb | **tokenizer 内无**（消融证明更好） |
| **骨干** | 线性注意力 Transformer（Linformer 式，4层8头） | temporal conv + ViT 风格（LN-QK，无 QKV bias） | ViT 式 encoder/predictor/reconstructor + momentum encoder | GPT 式因果 Transformer + SwiGLU（ETE）+ GAT（TEG） | GPT-2（causal） | 频率/时间/ temporal Transformer + 线性注意力下游 |
| **模型规模** | 3.2M | 5.8M / 46M / 369M（tokenizer 另 8.6M） | ~10M（变体 0.4M–101M） | 1.46M / 11.29M / 183.8M / **1.09B** | 254M / 500M / 1696M | ~1.9M（tokenizer 1.2M + 下游 0.7M） |
| **预训练数据** | 1000 万样本（PREST+SHHS+ECG） | ~2500 小时（约 20 数据集） | 5 数据集（PhysioMI/HGD/TSU/SEED/M3CV） | 3750 万单电极样本（~1B token） | ~25000 小时 | 4 EEG 数据集（另有 ear-EEG 跨设备验证） |
| **下游方式** | 微调 | 微调（线性探针差） | **Linear probing**（冻结 + 1×1 空间滤波器 + 线性头） | ETE 冻结 + TEG 多任务联合微调 | 指令微调（生成文本答案，单模型多任务） | masked token prediction 预训练 + 微调；**可插拔进 BIOT/LaBraM** |
| **多任务** | 否（逐任务微调） | 否 | 否（逐任务线性探针） | **是**（TEG 联合训练，验证协同增益） | **是**（指令微调单模型六任务） | 否（但组件可迁移） |
| **跨设备** | 通道表可扩展 | 受限于 10-20 空间 embedding | 受限（固定 58 通道布局） | 支持 138 电极任意组合 | 未验证 | **单通道设计，ear-EEG 验证最强** |

#### 7.2 核心分歧点解读

**① "token 到底是什么"——六篇的根本分野**

- BIOT：token = 规则切段的连续窗口，"tokenization"只是预处理；
- LaBraM：学出了 VQ 神经词表，但**只用于产生预训练的监督信号**（预测被 mask patch 的码字索引），推理时 tokenizer 被丢弃；
- TFM-Tokenizer 直接批评这一点，把学到的 motif token **真正作为下游模型的输入 embedding**，让"压缩 + 归纳偏置"的 tokenization 红利落到模型输入上；
- NeuroLM 走了第三条路：token 作为 **LLM 词表的扩展**，EEG 变成"外语句子"喂给 GPT-2；
- EEGPT 与 BrainGPT 则回避离散化：前者专注特征对齐+重构的自监督，后者用连续值自回归。

**② 预训练范式的三条路线**

- **对比学习**（BIOT：BYOL 式扰动-预测）→ 最早期的做法；
- **掩码建模**（LaBraM：掩码码字预测；EEGPT：对齐+重构双目标；TFM：掩码频谱图重构）→ 目前主流，其中掩码"目标"的设计是各家差异所在（离散码 / 表示 / 频谱图）；
- **自回归**（BrainGPT：连续值因果预测；NeuroLM：阶梯掩码下的离散码因果预测）→ 强调 EEG 的时序因果结构，BrainGPT 用消融证明同设定下 AR 优于 MAE 2%+。

**③ 空间（通道）异构的四种解法**

- 通道 embedding 表（BIOT）；
- 10-20 系统空间 embedding（LaBraM、NeuroLM）；
- 单通道独立建模（TFM-Tokenizer、BrainGPT 的电极级策略）——对非标准设备最友好；
- 图结构整合（BrainGPT 的 TEG：预训练图节点覆盖全电极，样本只激活子图）。

**④ 频域信息的地位递进**

BIOT 把 FFT 当特征工程的一种（能量向量）；LaBraM 把频谱当重构目标（发现相位贡献小）；NeuroLM 干脆去掉相位只留幅值+时域；TFM-Tokenizer 走得最远——把频率轴本身作为建模对象（频内 Transformer + 门控聚合 + 频带掩码）。这条线反映了社区共识的演进：**显式的时频结构建模比隐式期望模型自己学更重要**。

#### 7.3 演进脉络一句话

**BIOT**（2023）解决了"异构信号如何统一编码"（连续 token + 线性注意力）→ **LaBraM**（2024）证明"低信噪比 EEG 能学出离散语义码且大规模预训练有效"（VQ+频谱目标，但 token 只当靶子）→ **EEGPT**（2024）指出掩码目标不该是原始信号而应是高质量表示（双自监督+线性探针）→ **BrainGPT**（2024）把范式从掩码补全扭向自回归并冲到十亿参数 → **NeuroLM**（2025）把 token 真正接进 LLM 实现单模型多任务指令推理 → **TFM-Tokenizer**（2026）回到 tokenization 本身，给出第一个"学词表、可解释、跨设备、即插即用"的完整答案。

---

*总结基于六篇论文原文；实验数字均引自各论文报告值。*
