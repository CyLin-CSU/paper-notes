---
title: 预训练范式对比
tags: [预训练, 综述]
---

# 预训练范式对比

> 六篇论文恰好覆盖了自监督学习的三条路线：**对比学习、掩码建模、自回归**，且掩码建模内部还在持续进化。

## 三条路线总览

| 路线 | 论文 | 核心机制 | 关键设计 |
|---|---|---|---|
| **对比学习** | [BIOT](../papers/2026-09/0918-biot.md) | 扰动版预测原版表示（BYOL 式） | 丢通道+丢 token → predictor → 对比损失（T=0.2） |
| **掩码建模** | [LaBraM](../papers/2026-09/0918-labram.md) / [EEGPT](../papers/2026-09/0918-eegpt.md) / [TFM](../papers/2026-09/0918-tfm-tokenizer.md) | 看一部分，恢复另一部分 | 三家的"恢复目标"完全不同（见下） |
| **自回归** | [BrainGPT](../papers/2026-09/0918-braingpt.md) / [NeuroLM](../papers/2026-09/0918-neurolm.md) | 因果地预测下一单元 | BrainGPT 回归连续值；NeuroLM 预测离散码 |

## 掩码建模：预测目标的三次进化

EEG 低信噪比让"掩码后恢复什么"成了核心设计问题，三代方案一路升级：

| 代际 | 恢复目标 | 论文 | 动机 |
|---|---|---|---|
| 一代 | 原始波形（MSE） | （LaBraM 前期实验，**失败**） | EEG 随机、非平稳、低信噪比，loss 不收敛 |
| 二代 | 频谱（DFT 幅值+相位） | LaBraM | 频谱反映神经生理活动且稳定可学 |
| 2.5 代 | 时域信号 + 频域幅值 | NeuroLM | 发现相位贡献小，砍掉 |
| 三代 | **表示**（momentum encoder 的特征） | EEGPT | 信号空间难学，就在表示空间对齐（JEPA 思想） |
| 三代' | 掩码频谱图 | TFM-Tokenizer | 用于训练 tokenizer 本身 |

## 自回归 vs 掩码：范式之争

BrainGPT 给出了同架构、同损失度量下的直接对比（其 Table V）：

- **AR 全面优于 MAE，平均 +2% 以上**，与距离度量选择无关（ℓ2 最好，cos 最差）；
- 理由：EEG 反映连续渐进的信息流，过去神经活动影响未来状态，单向建模天然贴合；MAE 的双向重构破坏了信号的自然流向；
- 但注意代价：自回归只能用因果注意力，**看不到未来**——LaBraM/EEGPT 的双向建模在"整段理解型"任务上并非没有优势。

## 三种"掩码花样"

1. **对称掩码**（LaBraM 首创，TFM 沿用）：mask 与其补集各做一次 masked modeling——省一次 tokenizer 前向 + 一个样本两个互补视角（数据增强），大模型受益更明显；
2. **频带+时间掩码**（TFM）：消融显示随机掩码最差，频带掩码最关键（Kappa +8%），加时间掩码 balanced acc 再 +5%——**掩码的结构要匹配信号的结构**；
3. **阶梯掩码**（NeuroLM）：多通道场景下，同通道 token 预测同通道下一时刻，每个 token 可见所有通道的当前与历史时间步。

## 稳定性技巧清单

各家反复出现的训练技巧，值得记下：

- **EMA 更新目标侧**：LaBraM 更新 codebook、EEGPT 更新 momentum encoder（m=0.01）——防止目标漂移过快；
- **stop-gradient 成对损失**：codebook loss + commitment loss（VQ 三件套），把编码器和码字的更新解耦；
- **混入文本数据**（NeuroLM）：接 LLM 的模型每批喂少量纯文本，防语言能力灾难性遗忘；
- **只算答案部分的 loss**（NeuroLM 指令微调）：预测更稳定；
- **LayerNorm 归一化目标**（EEGPT 的 L_A 和 L_R 都对目标做 LN）：缓解极端值和协变量偏移。

## 关联论文

[BIOT](../papers/2026-09/0918-biot.md) · [LaBraM](../papers/2026-09/0918-labram.md) · [EEGPT](../papers/2026-09/0918-eegpt.md) · [BrainGPT](../papers/2026-09/0918-braingpt.md) · [NeuroLM](../papers/2026-09/0918-neurolm.md) · [TFM-Tokenizer](../papers/2026-09/0918-tfm-tokenizer.md)
