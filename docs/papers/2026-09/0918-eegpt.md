---
date: 2026-09-18
title: "EEGPT: Pretrained Transformer for Universal and Reliable Representation of EEG Signals"
authors: [Guagnyu Wang, Wenchao Liu, Yuhong He, Cong Xu, Lin Ma, Haifeng Li]
venue: "NeurIPS 2024"
year: 2024
tags: [EEG, 双自监督, 表示对齐, 线性探针, JEPA]
status: "精读"
rating: 4
code: "https://github.com/BINE022/EEGPT"
one-liner: "表示对齐 + 掩码重构双自监督的 10M 通用 EEG 特征提取器，linear probing 达 SOTA"
---
# EEGPT: Pretrained Transformer for Universal and Reliable Representation of EEG Signals

> **NeurIPS 2024**

EEGPT: Pretrained Transformer (NeurIPS 2024)

**作者**：Guagnyu Wang 等（哈尔滨工业大学）

#### 3.1 问题定位

EEG 低信噪比、被试间差异大、通道不匹配，导致掩码自编码器（MAE）学到的特征质量差、BERT 式模型没有显式表示 z。EEGPT 提出仅 ~10M 参数的通用特征提取器，用**双自监督**（时空表示对齐 + 掩码重构）训练，下游只做 **linear probing**。

#### 3.2 方法

**理论动机（式 1→2）**：标准 MAE 只有 `H(d_φ(z), x⊙(1−M))` 重构项，没有显式的 z；EEGPT 加一条表示对齐分支 `H(z, f_θ(x))`，显式地让 encoder 输出 z 携带全局语义（类似 MVEB 的最小充分表示），提升编码质量与泛化。

**局部时空 embedding**

- 58 电极、256Hz、输入 4 秒（T=1024）；每 patch 时间长度 d=64（250ms），共 N=16 个时间 patch；
- patch 线性嵌入 + **通道 embedding（Codex book）**：所有可学习通道向量 `{ς_i}` + 通道名→向量的映射 ℜ，**灵活对应任意数据集的通道配置**（通道适配的关键）；
- `token_{i,j} = Embed(p_{i,j}) + ς_i`。

**双自监督预训练**

1. **掩码方式（与 MAE 相反的关键设计）**：mask 掉 50% 时间 × 80% 通道的 patch，**encoder 处理的恰恰是被 mask 的稀疏部分**，且每个时间步追加 S 个可学习 **summary token**（类似 [CLS]）聚合信息；
2. **时空表示对齐（JEPA 风格，损失 L_A）**：
   - **Momentum encoder**（与 encoder 同构，EMA 动量 m=0.01）处理**全部** token（masked ∪ unmasked），作为预测目标 `menc_j`；
   - **Predictor**：拿 encoder 在 masked 部分的特征 + RoPE 旋转位置编码 + 可学习 query token，预测**全部时间段**的特征 `pred_j`；
   - 对齐损失：`L_A = −(1/N) Σ ‖pred_j, LN(menc_j)‖²`（LayerNorm 稳定训练）；
3. **掩码重构（MAE 风格，损失 L_R）**：
   - **Reconstructor**：encoder 特征（masked 部分）+ predictor 特征 + 位置信息 → 重构被 mask 部分的原始 patch；encoder→reconstructor 之间有 **skip connection**（保持特征、加速收敛）；
   - 重构损失：`L_R = −(1/|M|) Σ ‖rec_{i,j}, LN(p_{i,j})‖²`（目标也做 LayerNorm）；
4. 总损失 `L = L_A + L_R`。

**下游 Linear Probing**

- encoder 完全冻结，只加两个轻量模块：**adaptive spatial filter**（1×1 卷积，对齐数据通道与模型通道）+ 线性分类头；
- 只用 encoder 输出的 **summary token** 对应特征送入分类头；
- 目的：避免大数据模型在小样本微调下过拟合，同时让性能纯粹反映 encoder 本身的表示质量。

#### 3.3 创新点

1. **双自监督**：表示对齐（JEPA 式，在表示空间预测）+ 掩码重构（MAE 式，在信号空间重构）——显式表示 z，对抗低信噪比导致的特征质量差；
2. **掩码方向反转**：encoder 看被 mask 的稀疏部分、momentum encoder 看全量，迫使 encoder 输出含全局信息；
3. **通道 Codex book**（名字→向量映射）实现跨设备/跨通道配置适配；
4. **Linear probing 达到 SOTA**：证明学到的特征本身足够通用，小样本下游免微调；
5. 参数规模 scaling law 实证：`ACC = (33.6·N)^0.029`、`L_R = (0.72·N)^{−0.014}`。

#### 3.4 流程

```
EEG(58ch, 4s, 256Hz)
   │ 250ms 切 patch → 线性嵌入 ⊕ Codex book 通道 embedding
   │ mask 50%时间 × 80%通道
   ├─ masked 部分 + [SUM] tokens → Encoder ─┬→ Predictor(+RoPE, query) → 预测全部时段特征 ─┐
   │                                        └→(skip)                                      ├→ L_A 对齐
   └─ 全部 tokens → Momentum Encoder(EMA) ────────────────────────────────────────────────┘
   Encoder特征 + Predictor特征 → Reconstructor → 重构 masked patch → L_R
                                        ↓
下游：冻结 encoder → adaptive spatial filter → summary token → 线性头
```

#### 3.5 实验与结果

- 预训练：PhysioMI、HGD、TSU、SEED、M3CV（5 个数据集、多范式混合）；
- 下游：BCIC-2A/2B（运动想象）、Sleep-EDFx（睡眠分期）、KaggleERN、PhysioP300（ERP）、TUAB、TUEV；
- 结果：TUEV 上比 BIOT 提升 9.5% balanced acc；与 BENDR/BIOT/LaBraM 对比在多个任务领先（且对手往往是全量微调而 EEGPT 只线性探针）；
- 消融：去掉对齐损失 L_A 下游掉 6%~9%；去掉 predictor 会导致表示坍塌（重构 loss 不下降）；去掉 skip connection 掉 1%~3%；summary token 数量 S=4 较优。

---

## 架构图

![Figure 1 · 双自监督结构：encoder 看 masked 部分 + predictor 对齐 momentum 输出 + reconstructor 重构](../../assets/eegpt-arch.png)

*Figure 1 · 双自监督结构：encoder 看 masked 部分 + predictor 对齐 momentum 输出 + reconstructor 重构*


## 要点速览
!!! abstract "TL;DR"
    - ~10M 参数（8 个变体 0.4M–101M）；下游只用 linear probing 即达 SOTA
    - TUEV balanced acc 0.6232，比 BIOT（0.5281）高 9.5%
    - 双自监督：表示对齐（L_A，JEPA 式）+ 掩码重构（L_R，MAE 式）；掩码 50% 时间 × 80% 通道


## 与其他论文的关系

| 论文 / 工作 | 关系说明 |
|---|---|
| 思想上 | 承接 BYOL（momentum encoder）+ MAE（重构）+ JEPA（在表示空间预测）三条线 |
| LaBraM | 互补路线：LaBraM 走离散语义码，EEGPT 坚持连续表示但把自监督目标做得更好 |
| TFM-Tokenizer | 对照实验：EEGPT 依赖固定 58 通道布局的 Codex book，ear-EEG 跨设备实验无法参与 |

## 个人思考
- 把 linear probing 当评估协议本身就是贡献：冻结 encoder 后性能完全归因于表示质量，排除了微调技巧的干扰。
- 'encoder 看被 mask 的稀疏部分、momentum encoder 看全量'的反直觉设计，本质是用对齐任务逼迫稀疏视图输出全局语义（式 1→2 的显式表示 z）。
- 附录证明去掉 predictor 会表示坍塌（重构 loss 不再下降）——对齐分支必须保留 query/位置等余量，防止模型走捷径。

